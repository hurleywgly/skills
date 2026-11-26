/* Example final piece file (one artwork, rendered at 3840x2160 by final-template.html). */
const INKS={navy:'#22305c',cobalt:'#2f62b0',aqua:'#4aa3b8',sky:'#9cc3d6',coral:'#e36a50',blush:'#efbfae'};
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

const PIECE={fn:drift,seed:101,name:'Drift',media:MEDIA.riso};
