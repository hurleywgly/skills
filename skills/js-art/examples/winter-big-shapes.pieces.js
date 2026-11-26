/* Example pieces file: "winter, abstract, big shapes" in a mid-century print direction.
   Shows the pieces-file contract (INKS, META, PIECES) and most engine techniques. */
const INKS={navy:'#22305c',cobalt:'#2f62b0',aqua:'#4aa3b8',sky:'#9cc3d6',gold:'#e3a535',coral:'#e36a50',blush:'#efbfae'};
const META={title:'Blue December',sub:'Winter only, abstract, big shapes. Each print uses a different compositional idea.',
  inBounds:['Winter as weather and light: snow, ice, long nights, low sun','A few very large shapes','Blue-led palette with one small warm spark','A 16:9 still that reads from across the room'],
  outBounds:['Holiday objects','People, and anything literal from the brief','Small fussy detail','A clean vector look'],
  thesis:'Six ways to build a picture: strata, nested fields, cropped circles, light shards, pattern, and arcs.',
  recs:{ship:'Drift and Freeze.',follow:'Low Sun, First Snow and One Light.',skip:'Long Night is dark for a bright room. Northerly reads as motion more than winter. Half Blink is a holiday object.'},
  media:MEDIA.riso};

/* A ─ Drift */
function drift(p){
  let x=p.ink('sky');x.globalAlpha=.45;x.fillRect(0,0,W,H);
  x=p.ink('blush');const gl=q=>250+Math.sin(q/W*Math.PI*1.1+.5)*30;x.globalAlpha=.8;p.wpath(x,[...curve(gl,0,W),[W,480],[0,480]],2);x.fill();
  p.all(x=>{p.wcirc(x,1130,330,250,2);x.fill()});
  x=p.ink('coral');x.lineWidth=7;p.wcirc(x,1140,337,263,2);x.stroke();
  const B=[[380,'sky',.75,50,1.3,.3,3],[460,'aqua',.6,60,1.7,2.1,4],[540,'cobalt',.5,55,2.2,4,3],[620,'aqua',.9,65,1.4,1.2,5],[705,'cobalt',.9,48,2,5.2,5],[790,'navy',.9,36,1.6,3.3,4]];
  B.forEach(([y0,c,a,amp,fr,ph,n])=>{x=p.ink(c);const f=q=>y0+Math.sin(q/W*Math.PI*fr+ph)*amp,poly=[...curve(f,0,W),[W,H],[0,H]];
    x.globalAlpha=a;p.wpath(x,poly,1.5);x.fill();
    x=p.knock(c);p.strokes(x,()=>p.wpath(x,poly,0),{n:90,ang:.02,len:240,w:5,alpha:.06,spread:.04,box:[0,y0-amp,W,H-y0+amp]});
    p.contours(c,f,n,13)});
}

/* B ─ Low Sun */
function lowsun(p){
  const R=(x,a,b,w,h)=>p.wpath(x,[[a,b],[a+w,b],[a+w,b+h],[a,b+h]],1.5),hz=612;
  let x=p.ink('sky');x.globalAlpha=.5;x.fillRect(0,0,W,H);
  x=p.ink('blush');x.globalAlpha=.85;x.fillRect(0,540,W,72);
  x=p.ink('aqua');x.globalAlpha=.8;R(x,250,80,1150,740);x.fill();
  x=p.ink('cobalt');x.globalAlpha=.85;R(x,470,190,780,580);x.fill();
  x=p.ink('navy');R(x,650,290,440,420);x.fill();
  p.hatch('sky',[0,0,W,hz],0,9,.3);p.hatch('aqua',[250,80,1150,540],Math.PI/4,11,.28);p.hatch('cobalt',[470,190,780,430],-Math.PI/4,10,.3);p.hatch('navy',[650,290,440,330],Math.PI/2,9,.3);
  p.all(x=>{p.wcirc(x,870,548,106,1.5);x.fill()});
  x=p.ink('gold');p.wcirc(x,870,548,101,1.5);x.fill();
  x=p.ink('coral');x.lineWidth=5;x.beginPath();x.arc(873,551,108,-.2,2.1);x.stroke();
  p.all(x=>{let y=hz,i=0;while(y<H){const t=3+i*2.3;x.fillRect(0,y+p.r(-1,1),W,t);y+=t+Math.max(7,17-i*.6);i++}});
}

/* C ─ Freeze */
function freeze(p){
  let x=p.ink('sky');x.globalAlpha=.8;p.wcirc(x,300,860,560,2);x.fill();
  x=p.ink('aqua');x.globalAlpha=.85;p.wcirc(x,1260,160,400,2);x.fill();
  x=p.knock('aqua');x.lineWidth=3.5;x.globalAlpha=.4;for(let r=60;r<400;r+=42){x.beginPath();x.arc(1260,160,r+p.r(-3,3),0,7);x.stroke()}
  x=p.ink('cobalt');x.save();x.beginPath();x.arc(300,860,556,0,7);x.clip();p.dots(x,[0,300,860,600],10,(a,b)=>.7*Math.max(0,(a-300)/520));x.restore();
  x.globalAlpha=.9;p.wcirc(x,900,640,300,2);x.fill();
  x=p.knock('cobalt');x.lineWidth=2.4;for(let i=0;i<34;i++){const a=p.r(7),d=p.r(20,260),r=p.r(4,17);x.globalAlpha=p.r(.4,.85);x.beginPath();x.arc(900+Math.cos(a)*d,640+Math.sin(a)*d,r,0,7);p.R()<.25?x.fill():x.stroke()}
  x=p.ink('navy');p.wcirc(x,1390,730,150,1.5);x.fill();
  x=p.ink('coral');p.wcirc(x,610,230,34);x.fill();
  const segs=[];const crack=(a,b,ang,n,d)=>{for(let i=0;i<n;i++){const l=p.r(50,120);ang+=p.r(-.6,.6);const c=a+Math.cos(ang)*l,e=b+Math.sin(ang)*l;segs.push([a,b,c,e,d]);
    if(d<2&&p.R()<.35)crack(c,e,ang+p.r(.5,1.1)*(p.R()<.5?-1:1),Math.floor(n*.5),d+1);a=c;b=e}};
  crack(-20,420,.1,18,0);crack(700,-20,1.3,12,0);crack(1620,520,3.3,10,0);
  p.all(x=>segs.forEach(s=>{x.lineWidth=[6.5,4,2.4][s[4]];x.beginPath();x.moveTo(s[0],s[1]);x.lineTo(s[2],s[3]);x.stroke()}));
}

/* D ─ Long Night: organ-pipe aurora over a rising moon */
function longnight(p){
  let x=p.ink('navy');x.fillRect(0,0,W,H);
  x=p.knock('navy');p.strokes(x,null,{n:200,ang:.1,len:240,w:10,alpha:.04,spread:.1});
  for(let i=0;i<90;i++){x.globalAlpha=p.r(.4,1);x.beginPath();x.arc(p.r(W),p.r(0,760),p.r(.8,2.6),0,7);x.fill()}
  const pipe=(sx,w,yb,c,ka,ia)=>{const poly=[[sx,-10],[sx+w,-10],[sx+w,yb],[sx,yb+p.r(-22,22)]];x=p.knock('navy');x.globalAlpha=ka;p.wpath(x,poly,1);x.fill();x=p.ink(c);x.globalAlpha=ia;p.wpath(x,poly,1);x.fill()};
  const b1=q=>400+Math.sin(q/210+1)*130+Math.sin(q/77)*40,b2=q=>250+Math.sin(q/160+3)*90;
  for(let sx=520;sx<W;sx+=31)pipe(sx,p.r(15,29),b1(sx)+p.r(-45,45),(Math.round(sx/31)%3)?'aqua':'sky',p.r(.35,.7),p.r(.5,.9));
  for(let sx=180;sx<1250;sx+=44)pipe(sx,p.r(8,16),b2(sx)+p.r(-50,50),'sky',p.r(.2,.4),p.r(.4,.7));
  x=p.knock('navy');p.wcirc(x,470,1010,500,2);x.fill();
  const gr=q=>806+Math.sin(q/W*Math.PI*1.6+2)*22,ground=[...curve(gr,0,W),[W,H],[0,H]];p.wpath(x,ground,1.5);x.fill();
  x=p.ink('sky');x.save();x.beginPath();x.arc(470,1010,497,0,7);x.clip();p.dots(x,[0,480,1000,340],11,(a,b)=>.9*Math.max(0,(a-300)/650));x.restore();
  x.globalAlpha=.55;p.wpath(x,ground,1.5);x.fill();p.contours('sky',gr,3,16);
  x=p.knock('navy');p.wcirc(x,1330,650,20);x.fill();x=p.ink('coral');p.wcirc(x,1330,650,17);x.fill();
}

/* E ─ First Snow */
function firstsnow(p){
  const f=q=>690+Math.sin(q/W*Math.PI*1.3+.4)*70,g=q=>f(q)+40+Math.sin(q/W*Math.PI)*120,h=q=>g(q)+90+Math.sin(q/W*Math.PI*2+1)*30;
  let x=p.ink('cobalt');x.globalAlpha=.92;x.fillRect(0,0,W,H);p.hatch('cobalt',[0,0,W,H],Math.PI/2.6,12,.16,1.6);
  const N=makeNoise(77),ds=[];
  for(let r=0;r<9;r++)for(let c=-1;c<18;c++){const px=c*100+(r%2?50:0)+p.r(-7,7),py=36+r*82+p.r(-7,7),rad=(5+r*3.2)*(.5+1.1*N(px/260,py/260));if(py+rad>f(px)-10)continue;ds.push([px,py,rad,p.R()])}
  x=p.knock('cobalt');ds.forEach(d=>{if(d[2]>19&&d[3]>.5&&d[3]<.72){x.lineWidth=d[2]*.3;x.lineCap='round';for(let k=0;k<3;k++){const a=k*Math.PI/3+.2;x.beginPath();x.moveTo(d[0]-Math.cos(a)*d[2]*1.2,d[1]-Math.sin(a)*d[2]*1.2);x.lineTo(d[0]+Math.cos(a)*d[2]*1.2,d[1]+Math.sin(a)*d[2]*1.2);x.stroke()}}else{p.wcirc(x,d[0],d[1],d[2],1);x.fill()}});
  p.wpath(x,[...curve(f,0,W),[W,H],[0,H]],2);x.fill();
  x=p.ink('sky');ds.forEach(d=>{if(d[3]<.22){p.wcirc(x,d[0],d[1],d[2]-1,1);x.fill()}});
  x=p.ink('gold');ds.forEach(d=>{if(d[3]>.965){p.wcirc(x,d[0],d[1],d[2]-1,1);x.fill()}});
  x=p.ink('sky');x.save();p.wpath(x,[...curve(f,0,W),[W,H],[0,H]],0);x.clip();p.dots(x,[0,560,W,340],10,(a,b)=>.8*Math.max(0,1-(b-f(a))/110)*Math.max(0,(a-500)/1100));x.restore();
  x=p.ink('aqua');x.globalAlpha=.75;p.wpath(x,[...curve(g,0,W),[W,H],[0,H]],2);x.fill();p.contours('aqua',g,3,15);
  x=p.ink('navy');p.wpath(x,[...curve(h,0,W),[W,H],[0,H]],2);x.fill();p.contours('navy',h,3,13);
}

/* F ─ Northerly: one gust as a supergraphic */
function northerly(p){
  const O=[-220,1260],B=[[430,80,'navy',1],[545,120,'cobalt',.9],[690,160,'sky',.85],[850,64,'aqua',.9],[944,190,'cobalt',.55],[1134,96,'aqua',.5],[1270,220,'sky',.5],[1490,84,'navy',.85],[1574,400,'sky',.3]];
  let x;B.forEach(([r,w,c,a])=>{x=p.ink(c);x.globalAlpha=a;x.lineWidth=w;x.beginPath();x.arc(O[0],O[1],r+w/2,0,7);x.stroke()});
  x=p.knock('cobalt');x.lineWidth=2;for(let r=556;r<660;r+=11){x.globalAlpha=.4;x.beginPath();x.arc(O[0],O[1],r,0,7);x.stroke()}
  x=p.knock('sky');x.lineWidth=2;for(let r=1284;r<1480;r+=15){x.globalAlpha=.45;x.beginPath();x.arc(O[0],O[1],r,0,7);x.stroke()}
  x=p.ink('cobalt');x.save();x.beginPath();x.arc(O[0],O[1],1134,0,7);x.arc(O[0],O[1],944,0,7,true);x.clip();p.dots(x,[0,0,W,H],11,(a,b)=>.75*Math.max(0,1-a/1100));x.restore();
  x=p.ink('gold');x.lineWidth=13;x.beginPath();x.arc(O[0],O[1],928,0,7);x.stroke();
  p.all(x=>{p.wcirc(x,1180,300,168,2);x.fill()});
  x=p.ink('blush');x.globalAlpha=.9;p.wcirc(x,1180,300,160,2);x.fill();
  x=p.ink('coral');p.wcirc(x,985,470,24);x.fill();
}

/* 4 (remake) ─ Half Blink */
function halfblink2(p){
  let x=p.ink('navy');x.fillRect(0,0,W,H);
  x=p.knock('navy');p.strokes(x,null,{n:200,ang:.1,len:240,w:10,alpha:.04,spread:.1});
  const blocks=[[0,230,620],[230,180,700],[410,260,560],[670,150,740],[820,300,640],[1120,200,520],[1320,280,690]],wins=[];
  blocks.forEach(([a,w,y])=>{x=p.knock('navy');x.globalAlpha=.7;p.wpath(x,[[a,y],[a+w,y],[a+w,H],[a,H]],1.5);x.fill();
    x=p.ink('cobalt');p.wpath(x,[[a,y],[a+w,y],[a+w,H],[a,H]],1.5);x.fill();
    for(let k=0;k<3;k++)wins.push([a+p.r(20,w-50),y+p.r(30,Math.max(40,H-y-70))])});
  ['navy','cobalt'].forEach(n=>{x=p.knock(n);wins.forEach(q=>x.fillRect(q[0],q[1],26,34))});
  x=p.ink('gold');wins.forEach(q=>x.fillRect(q[0]+2,q[1]+2,24,32));
  x=p.knock('navy');p.wcirc(x,1390,150,72);x.fill();x=p.ink('navy');p.wcirc(x,1420,132,64);x.fill();
  const cat=(a,b,c,d,s,n)=>{const o=[];for(let i=0;i<=n;i++){const t=i/n;o.push([a+(c-a)*t,b+(d-b)*t+s*4*t*(1-t)])}return o};
  const S=[cat(-20,130,1620,230,230,24),cat(-20,430,1620,330,150,20)],cols=['gold','coral','sky','aqua','gold','coral'],bulbs=[];
  S.forEach((s,si)=>s.forEach((q,i)=>{if(i%2&&i<s.length-1)bulbs.push({x:q[0],y:q[1]+46,c:cols[(i+si*3>>1)%cols.length],dead:(si==0&&i==9)||(si==1&&i==13),off:(si==0&&i==17)?16:0})}));
  bulbs.forEach(b=>{if(b.dead)return;['navy','cobalt'].forEach(n=>{x=p.knock(n);const g=x.createRadialGradient(b.x,b.y,20,b.x,b.y,105);g.addColorStop(0,'rgba(0,0,0,.4)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(b.x-110,b.y-110,220,220)})});
  ['navy','cobalt'].forEach(n=>{x=p.knock(n);x.lineWidth=3;x.globalAlpha=.7;S.forEach(s=>{x.beginPath();s.forEach((q,i)=>i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]));x.stroke()});
    x.globalAlpha=1;bulbs.forEach(b=>{x.beginPath();x.ellipse(b.x,b.y,31,41,0,0,7);x.fill();x.fillRect(b.x-9,b.y-56,18,18)})});
  bulbs.forEach(b=>{if(b.dead){x=p.ink('navy');x.beginPath();x.ellipse(b.x,b.y,26,36,0,0,7);x.fill();return}
    x=p.ink(b.c);x.beginPath();x.ellipse(b.x+b.off,b.y+b.off*.6,29,39,p.r(-.08,.08),0,7);x.fill();
    x=p.knock(b.c);x.globalAlpha=.75;x.beginPath();x.ellipse(b.x+b.off-11,b.y+b.off*.6-12,4.5,12,.35,0,7);x.fill()});
}

/* 6 (remake) ─ One Light */
function onelight2(p){
  const L=[1010,380];let x=p.ink('navy');x.fillRect(0,0,W,H);
  x=p.knock('navy');p.strokes(x,null,{n:200,ang:.15,len:240,w:10,alpha:.04,spread:.1});
  for(let i=0;i<60;i++){x.globalAlpha=p.r(.3,.9);x.beginPath();x.arc(p.r(W),p.r(H),p.r(.8,2.4),0,7);x.fill()}
  [[440,.12],[330,.16],[232,.22],[146,.3]].forEach(([r,a])=>{x.globalAlpha=a;p.wcirc(x,...L,r,2.5);x.fill()});
  x.globalAlpha=1;p.wcirc(x,...L,46,1.5);x.fill();
  [[60,1060,620,'sky',.85],[640,1220,500,'aqua',.8]].forEach(([a,b,r,c,al])=>{x=p.knock('navy');x.globalAlpha=.92;p.wcirc(x,a,b,r,2.5);x.fill();x=p.ink(c);x.globalAlpha=al;p.wcirc(x,a,b,r,2.5);x.fill();
    x=p.knock(c);x.lineWidth=2.2;for(let k=1;k<5;k++){x.globalAlpha=.4;x.beginPath();x.arc(a,b,r-k*17,0,7);x.stroke()}});
  const fn=(a,b)=>{const d=Math.hypot(a-L[0],b-L[1]);return d<56||d>215?0:(1-(d-56)/160)*.95};
  x=p.knock('navy');x.globalAlpha=.8;p.dots(x,[L[0]-220,L[1]-220,440,440],13,fn,.35);
  x=p.ink('gold');p.dots(x,[L[0]-220,L[1]-220,440,440],13,(a,b)=>fn(a,b)*.85,.35);
  p.wcirc(x,...L,38,1.5);x.fill();
  x=p.knock('gold');p.wcirc(x,...L,15);x.fill();x=p.ink('coral');p.wcirc(x,...L,14);x.fill();
}

const PIECES=[
 {fn:drift,seed:101,label:'New · A',name:'Drift',tag:'Six snowdrifts under a white sun with a thin coral rim.',tech:'Wave strata with wind-carved contour lines, blush alpenglow, knockout sun',pal:['sky','blush','aqua','cobalt','navy','coral'],fit:5,risk:''},
 {fn:lowsun,seed:113,label:'New · B',name:'Low Sun',tag:'Nested color fields, a frozen lake, and the 4pm sun.',tech:'Cross-hatched nested rectangles, reflection cut into widening bars',pal:['sky','blush','aqua','cobalt','navy','gold','coral'],fit:5,risk:'The most geometric of the set. It could read cool or severe.'},
 {fn:freeze,seed:127,label:'New · C',name:'Freeze',tag:'Giant discs of ice, cropped by the frame and cracked right through.',tech:'Oversized circles, trapped-air bubbles, cracks knocked through every ink at once',pal:['sky','aqua','cobalt','navy','coral'],fit:5,risk:''},
 {fn:longnight,seed:131,label:'New · D',name:'Long Night',tag:'An aurora built like organ pipes over a huge rising moon.',tech:'Pleated light curtains from stepped stripes, cropped halftone moon',pal:['navy','aqua','sky','coral'],fit:4,risk:'Dark overall. It may look heavy in a bright room.'},
 {fn:firstsnow,seed:139,label:'New · E',name:'First Snow',tag:'Snowfall as a textile pattern, growing as it falls toward one white hill.',tech:'Staggered dot grid scaled for depth, a few flakes cut as asterisks or re-inked',pal:['cobalt','sky','aqua','navy','gold'],fit:5,risk:''},
 {fn:northerly,seed:149,label:'New · F',name:'Northerly',tag:'One long gust drawn as a supergraphic, sweeping past a pale sun.',tech:'Concentric arc bands from an off-canvas center, one gold pinstripe',pal:['navy','cobalt','sky','aqua','gold','blush','coral'],fit:4,risk:'The least wintry. It reads as motion more than as a season.'},
 {fn:halfblink2,seed:157,label:'Remake · 4',name:'Half Blink',tag:'The same joke, told with big shapes: a few bulbs are wrong.',tech:'Oversized bulbs with knockout glow, one dead per string, one misregistered',pal:['navy','cobalt','gold','coral','sky','aqua'],fit:4,risk:'Still the most literal holiday object on the page.'},
 {fn:onelight2,seed:163,label:'Remake · 6',name:'One Light',tag:'One warm point with a stepped halo and two quiet arcs.',tech:'Flat stepped halo rings, halftone gold corona, contour-lined arcs',pal:['navy','sky','aqua','gold','coral'],fit:5,risk:''},
];

