/* Pure Beta formulas; positive shape parameters. Independently checked against SciPy. */
const BetaMath = (() => {
  function logGamma(z) {
    const c=[676.5203681218851,-1259.1392167224028,771.3234287776531,-176.6150291621406,12.507343278686905,-0.13857109526572012,9.984369578019572e-6,1.5056327351493116e-7];
    if(z<0.5)return Math.log(Math.PI)-Math.log(Math.sin(Math.PI*z))-logGamma(1-z);
    z-=1;let x=0.9999999999998099;
    c.forEach((v,i)=>x+=v/(z+i+1));const t=z+7.5;
    return 0.5*Math.log(2*Math.PI)+(z+0.5)*Math.log(t)-t+Math.log(x);
  }
  const logBeta=(a,b)=>logGamma(a)+logGamma(b)-logGamma(a+b);
  function pdf(x,a,b){
    if(!(a>0&&b>0))throw Error('Positive shapes required');
    if(x<0||x>1)return 0;
    if(x===0)return a<1?Infinity:a===1?b:0;
    if(x===1)return b<1?Infinity:b===1?a:0;
    return Math.exp((a-1)*Math.log(x)+(b-1)*Math.log1p(-x)-logBeta(a,b));
  }
  const mean=(a,b)=>a/(a+b);
  const variance=(a,b)=>a*b/((a+b)**2*(a+b+1));
  const posterior=(a,b,s,f)=>({a:a+s,b:b+f,mean:mean(a+s,b+f),sd:Math.sqrt(variance(a+s,b+f))});
  return {logGamma,logBeta,pdf,mean,variance,posterior};
})();
if(typeof module!=='undefined')module.exports=BetaMath;
