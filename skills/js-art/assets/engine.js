/* js-art print engine
   Layered-ink printmaking simulation for Canvas 2D (riso, screen print, gouache, cut paper, woodblock).
   Draw in a 1600×900 design space; `scale` renders it larger (2.4 → 3840×2160).
   Model: every ink is its own offscreen layer. White is never painted: knock() cuts a layer so paper shows.
   finish() roughens each layer's edges, grains it, and multiplies it onto paper with slight misregistration. */
const W=1600,H=900;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function makeNoise(seed){const R=rng(seed),N=256,t=new Float32Array(N*N);for(let i=0;i<t.length;i++)t[i]=R();
  const f=(x,y)=>{const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;const a=t[(yi&255)*N+(xi&255)],b=t[(yi&255)*N+((xi+1)&255)],c=t[((yi+1)&255)*N+(xi&255)],d=t[((yi+1)&255)*N+((xi+1)&255)];const u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v};
  return (x,y)=>f(x,y)*0.6+f(x*2.1+7,y*2.1+3)*0.3+f(x*4.3+1,y*4.3+9)*0.1;}
/* sample y=f(x) into points, for building wavy polygons */
const curve=(f,x0,x1,step=16)=>{const a=[];for(let x=x0;x<=x1+0.1;x+=step)a.push([x,f(x)]);return a};
const rot=(q,c,a)=>[c[0]+(q[0]-c[0])*Math.cos(a)-(q[1]-c[1])*Math.sin(a),c[1]+(q[0]-c[0])*Math.sin(a)+(q[1]-c[1])*Math.cos(a)];

/* Media profiles: how rough, grainy and misregistered the print is. Pass one as `media`, or override keys. */
const MEDIA={
  riso:      {warpFine:3.4,warpCoarse:4.5,grain:.30,mottle:.28,speckle:.012,misreg:3,  paperGrain:.07,vignette:.22,fibers:900},
  screen:    {warpFine:1.6,warpCoarse:2.0,grain:.14,mottle:.16,speckle:.004,misreg:2,  paperGrain:.05,vignette:.15,fibers:500},
  gouache:   {warpFine:2.4,warpCoarse:7.0,grain:.12,mottle:.40,speckle:.002,misreg:.5, paperGrain:.08,vignette:.18,fibers:1200},
  cutpaper:  {warpFine:.8, warpCoarse:5.0,grain:.08,mottle:.10,speckle:0,   misreg:0,  paperGrain:.09,vignette:.12,fibers:1600},
  woodblock: {warpFine:2.8,warpCoarse:3.0,grain:.22,mottle:.34,speckle:.008,misreg:1.5,paperGrain:.10,vignette:.20,fibers:2200},
};

class Print{
  /* o: {seed, scale, inks:{name:'#hex'}, paper:[r,g,b], media: MEDIA.x or overrides} */
  constructor(cv,o={}){const{seed=1,scale=1,inks={},paper=[239,230,210],media={}}=o;
    this.S=scale;this.PW=Math.round(W*scale);this.PH=Math.round(H*scale);cv.width=this.PW;cv.height=this.PH;
    this.ctx=cv.getContext('2d',{willReadFrequently:true});this.R=rng(seed);this.seed=seed;this.C=inks;this.paperRGB=paper;
    this.m=Object.assign({},MEDIA.riso,media);this.order=[];this.map={};}
  r(a,b){if(b===undefined){b=a;a=0}return a+(b-a)*this.R()}
  /* get an ink layer ready to draw on (creates it on first use; print order = first-use order) */
  ink(n){if(!this.C[n])throw new Error('unknown ink: '+n);
    if(!this.map[n]){const c=document.createElement('canvas');c.width=this.PW;c.height=this.PH;const x=c.getContext('2d',{willReadFrequently:true});x.setTransform(this.S,0,0,this.S,0,0);this.map[n]=x;this.order.push(n)}
    const x=this.map[n];x.globalCompositeOperation='source-over';x.globalAlpha=1;x.setLineDash([]);x.fillStyle=x.strokeStyle=this.C[n];x.lineCap='round';x.lineJoin='round';return x}
  /* same layer, but drawing now erases ink so the paper (or inks beneath) shows through */
  knock(n){const x=this.ink(n);x.globalCompositeOperation='destination-out';x.fillStyle=x.strokeStyle='#000';return x}
  /* run fn(ctx) as a knockout on every layer created so far: cracks, horizon cuts, clean beds for warm inks */
  all(fn){this.order.slice().forEach(n=>fn(this.knock(n)))}

  /* ── hand-wobbled paths (build a path; caller fills or strokes) ── */
  wpath(x,pts,j=2,closed=true){const o=[],n=pts.length,segs=closed?n:n-1;
    for(let s=0;s<segs;s++){const[a,b]=pts[s],[c,d]=pts[(s+1)%n];const k=Math.max(1,Math.round(Math.hypot(c-a,d-b)/14));
      for(let t=0;t<k;t++){const u=t/k;o.push([a+(c-a)*u+this.r(-j,j),b+(d-b)*u+this.r(-j,j)])}}
    if(!closed)o.push(pts[n-1]);x.beginPath();o.forEach((q,i)=>i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]));if(closed)x.closePath()}
  wcirc(x,cx,cy,r,j=1.2){x.beginPath();const k=Math.max(24,Math.round(r/2.5));for(let i=0;i<k;i++){const a=i/k*Math.PI*2,rr=r+this.r(-j,j);i?x.lineTo(cx+Math.cos(a)*rr,cy+Math.sin(a)*rr):x.moveTo(cx+Math.cos(a)*rr,cy+Math.sin(a)*rr)}x.closePath()}
  /* lobed organic shape: k lobes of depth amp (kidney k=2, clover k=3–4, frond k=5+) */
  lob(x,cx,cy,r,k,amp,ph=0,sx=1,j=2,ra=0){x.beginPath();const n=140;for(let i=0;i<n;i++){const a=i/n*Math.PI*2,rr=r*(1+amp*Math.sin(k*a+ph)+amp*.3*Math.sin((k+1)*a+ph*1.7))+this.r(-j,j);const q=rot([cx+Math.cos(a)*rr*sx,cy+Math.sin(a)*rr],[cx,cy],ra);i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1])}x.closePath()}
  star(x,cx,cy,r,a=0,pts=5,inner=0.45){x.beginPath();for(let i=0;i<pts*2;i++){const rr=i%2?r*inner:r,t=a+i/(pts*2)*Math.PI*2-Math.PI/2;const px=cx+Math.cos(t)*rr+this.r(-1,1),py=cy+Math.sin(t)*rr+this.r(-1,1);i?x.lineTo(px,py):x.moveTo(px,py)}x.closePath()}
  boomer(x,cx,cy,s,a){const P=q=>rot([cx+q[0]*s,cy+q[1]*s],[cx,cy],a);const t1=P([-1,.25]),co=P([0,-1]),t2=P([1,.25]),ci=P([0,-.3]);
    x.beginPath();x.moveTo(...t1);x.quadraticCurveTo(...co,...t2);x.quadraticCurveTo(...ci,...t1);x.closePath()}

  /* ── interior texture ── */
  /* many short brush strokes, optionally clipped to clip() path. On a knock() ctx this is dry-brush. */
  strokes(x,clip,o){const{n=400,ang=0,len=40,w=6,alpha=0.2,spread=0.2,box=[0,0,W,H]}=o;x.save();if(clip){clip();x.clip()}x.globalAlpha=alpha;
    for(let i=0;i<n;i++){const px=this.r(box[0],box[0]+box[2]),py=this.r(box[1],box[1]+box[3]),a=ang+this.r(-spread,spread),l=len*this.r(0.5,1.3);x.lineWidth=w*this.r(0.5,1.2);
      x.beginPath();x.moveTo(px,py);x.quadraticCurveTo(px+Math.cos(a)*l/2+this.r(-3,3),py+Math.sin(a)*l/2+this.r(-3,3),px+Math.cos(a)*l,py+Math.sin(a)*l);x.stroke()}x.restore()}
  /* halftone dot field over box; fn(x,y) returns dot size 0..1 */
  dots(x,box,step,fn,ang=0.4){const[bx,by,bw,bh]=box,c=Math.cos(ang),s=Math.sin(ang),D=Math.hypot(bw,bh),cx=bx+bw/2,cy=by+bh/2;
    for(let u=-D/2;u<D/2;u+=step)for(let v=-D/2;v<D/2;v+=step){const px=cx+u*c-v*s,py=cy+u*s+v*c;if(px<bx||py<by||px>bx+bw||py>by+bh)continue;const t=fn(px,py);if(t<=0.03)continue;
      x.beginPath();x.arc(px,py,step*0.56*Math.min(1,t)*this.r(0.85,1.1),0,7);x.fill()}}
  /* parallel knocked-out lines across a box (cross-hatching, wood grain, weave) */
  hatch(c,box,ang,gap,alpha,lw=1.8){const x=this.knock(c);x.save();x.beginPath();x.rect(...box);x.clip();x.lineWidth=lw;const D=Math.hypot(box[2],box[3]),cx=box[0]+box[2]/2,cy=box[1]+box[3]/2,co=Math.cos(ang),si=Math.sin(ang);
    for(let v=-D/2;v<D/2;v+=gap){x.globalAlpha=alpha*this.r(.6,1.2);const o=this.r(-1.5,1.5);x.beginPath();x.moveTo(cx-co*D/2-si*(v+o),cy-si*D/2+co*(v+o));x.lineTo(cx+co*D/2-si*(v-o),cy+si*D/2+co*(v-o));x.stroke()}x.restore()}
  /* n knocked-out lines that echo the curve y=f(x) just below it (wind lines, contour, water) */
  contours(c,f,n,gap){const x=this.knock(c);x.lineWidth=2.2;for(let k=1;k<=n;k++){x.globalAlpha=this.r(.25,.55);const d=k*gap+this.r(-3,3),ph=this.r(7),a=this.r(-100,W*.55),b=a+this.r(350,950);
    x.beginPath();curve(q=>f(q)+d+Math.sin(q/140+ph)*3,a,b,12).forEach((q,i)=>i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]));x.stroke()}}
  burst(x,cx,cy,r,n=8,w=2){x.lineWidth=w;for(let i=0;i<n;i++){const a=i/n*Math.PI*2+this.r(-0.06,0.06),l=r*(i%2?0.55:1)*this.r(0.9,1.05),ex=cx+Math.cos(a)*l,ey=cy+Math.sin(a)*l;
      x.beginPath();x.moveTo(cx,cy);x.lineTo(ex,ey);x.stroke();x.beginPath();x.arc(ex,ey,w*1.3,0,7);x.fill()}}

  /* ── printing ── */
  texture(x,seed){const PW=this.PW,PH=this.PH,S=this.S,m=this.m,s=x.getImageData(0,0,PW,PH).data,out=x.createImageData(PW,PH),d=out.data,R=rng(seed),N=makeNoise(seed),M=makeNoise(seed+13);
    const wf=m.warpFine*S,wc=m.warpCoarse*S;
    for(let y=0;y<PH;y++){const v=y/S;for(let xx=0;xx<PW;xx++){const u=xx/S;
      let ox=Math.round(xx+(N(u/3.2,v/3.2)-.5)*wf+(M(u/46,v/46)-.5)*wc),oy=Math.round(y+(N(u/3.2+90,v/3.2+40)-.5)*wf+(M(u/46+31,v/46+77)-.5)*wc);
      ox=ox<0?0:ox>=PW?PW-1:ox;oy=oy<0?0:oy>=PH?PH-1:oy;const j=(oy*PW+ox)*4,a=s[j+3];if(!a)continue;const i=(y*PW+xx)*4;
      let k=(1-m.mottle*.7)+m.mottle*M(u/55+5,v/55+5)+(R()-.5)*m.grain;if(R()<m.speckle)k*=.1;d[i]=s[j];d[i+1]=s[j+1];d[i+2]=s[j+2];d[i+3]=a*k}}
    x.putImageData(out,0,0)}
  /* call once after drawing. async so a 4K render doesn't freeze the page; tick(label) reports progress. */
  async finish(tick){const m=this.ctx,PW=this.PW,PH=this.PH,S=this.S,P=this.paperRGB,mm=this.m,pause=()=>new Promise(r=>setTimeout(r,0));
    m.setTransform(1,0,0,1,0,0);m.globalCompositeOperation='source-over';m.fillStyle=`rgb(${P[0]},${P[1]},${P[2]})`;m.fillRect(0,0,PW,PH);
    for(let i=0;i<this.order.length;i++){const n=this.order[i],x=this.map[n];if(tick)tick('inking '+n);await pause();
      this.texture(x,this.seed*31+i*7);m.globalCompositeOperation='multiply';m.drawImage(x.canvas,this.r(-mm.misreg,mm.misreg)*S,this.r(-mm.misreg,mm.misreg)*S)}
    m.globalCompositeOperation='source-over';if(tick)tick('paper');await pause();
    const id=m.getImageData(0,0,PW,PH),d=id.data,R=rng(this.seed+99),N=makeNoise(this.seed+5);
    for(let y=0;y<PH;y++)for(let x=0;x<PW;x++){const i=(y*PW+x)*4,dx=(x-PW/2)/PW,dy=(y-PH/2)/PH,g=(1-mm.vignette*(dx*dx+dy*dy))*(0.97+0.05*N(x/S/9,y/S/9)+(R()-0.5)*mm.paperGrain);d[i]*=g;d[i+1]*=g;d[i+2]*=g}
    m.putImageData(id,0,0);m.globalAlpha=0.06;m.strokeStyle='#5a4a30';m.lineWidth=0.6*S;
    for(let k=0;k<mm.fibers*S;k++){const x=this.r(PW),y=this.r(PH),a=this.r(7),l=this.r(4,14)*S;m.beginPath();m.moveTo(x,y);m.quadraticCurveTo(x+Math.cos(a+.6)*l/2,y+Math.sin(a+.6)*l/2,x+Math.cos(a)*l,y+Math.sin(a)*l);m.stroke()}
    m.globalAlpha=1}
}
