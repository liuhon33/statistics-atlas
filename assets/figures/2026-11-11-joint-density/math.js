(function(root){
  'use strict';
  const phi=z=>Math.exp(-z*z/2)/Math.sqrt(2*Math.PI);
  const valid=rho=>{if(!Number.isFinite(rho)||Math.abs(rho)>=1)throw new RangeError('Use |rho| < 1.');};
  const normal=(x,mean,variance)=>phi((x-mean)/Math.sqrt(variance))/Math.sqrt(variance);
  const joint=(x,y,rho,mux=0)=>{valid(rho);const u=x-mux,v=1-rho*rho;return Math.exp(-(u*u-2*rho*u*y+y*y)/(2*v))/(2*Math.PI*Math.sqrt(v));};
  const conditionalX=(x,y,rho,mux=0)=>{valid(rho);return normal(x,mux+rho*y,1-rho*rho);};
  const conditionalY=(y,x,rho,mux=0)=>{valid(rho);return normal(y,rho*(x-mux),1-rho*rho);};
  const values=(y0,x0,rho,mux=0)=>{valid(rho);return {meanX:mux+rho*y0,meanY:rho*(x0-mux),variance:1-rho*rho,areaX:phi(y0),areaY:phi(x0-mux),totalMean:mux};};
  // Orthographic screen coordinates: camera changes representation, never the density.
  const project=(x,y,z,azimuth,elevation)=>{
    const c=Math.cos(azimuth),s=Math.sin(azimuth),ce=Math.cos(elevation),se=Math.sin(elevation);
    const horizontal=c*x-s*y,depth=s*x+c*y;
    return [horizontal,depth*se-z*ce,depth*ce+z*se];
  };
  const api={phi,normal,joint,conditionalX,conditionalY,values,project};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.JointDensityMath=api;
})(typeof globalThis!=='undefined'?globalThis:this);
