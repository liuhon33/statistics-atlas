const PcaMath = (() => {
  const a = [-6,-5,-4,-3,-2,-1,1,2,3,4,5,6];
  const b = [1,-1,1,-1,1,-1,-1,1,-1,1,-1,1];
  const points = a.map((x,i)=>[(x+b[i])/Math.SQRT2,(x-b[i])/Math.SQRT2]);
  function project(degrees){
    const angle=degrees*Math.PI/180, v=[Math.cos(angle),Math.sin(angle)];
    const scores=points.map(p=>p[0]*v[0]+p[1]*v[1]);
    const feet=scores.map(t=>v.map(x=>x*t));
    const ss=scores.reduce((sum,t)=>sum+t*t,0);
    const error=points.reduce((sum,p,i)=>sum+(p[0]-feet[i][0])**2+(p[1]-feet[i][1])**2,0);
    return {v,scores,feet,variance:ss/11,error:error/11,fraction:ss/194};
  }
  return {points,project};
})();
if(typeof module!=='undefined') module.exports=PcaMath;
