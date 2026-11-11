// Mathematical regression checks for the interactive calculation engine.
const assert=require('node:assert/strict'),M=require('./math.js');
const near=(a,b,tol=1e-6)=>assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);
for(const family of ['normal','logistic'])for(const sig of [1,2.5,5]){
 const m=M.model(family,sig),eps=1e-4;
 for(const y of [-3,1,5,8,15])for(const mu of [0,5,10]){
  near((m.log(y,mu+eps)-m.log(y,mu-eps))/(2*eps),m.score(y,mu));
  near((m.score(y,mu+eps)-m.score(y,mu-eps))/(2*eps),m.hessian(y,mu));
 }
}
for(const a of [.25,1,7,9])for(const b of [.25,1,5,9])for(const phi of [-1.4,0,.7,1.5]){
 const S=M.covariance(a,b,phi),I=M.inv(S),v=[Math.cos(phi),Math.sin(phi)];
 for(const e of [[1,0],[0,1]])M.mv(I,M.mv(S,e)).forEach((x,i)=>near(x,e[i]));
 near(M.quad(I,v),1/a);
 for(const pt of M.ellipse(a,b,phi))near(M.quad(I,pt),1);
 for(const pt of M.ellipse(1/a,1/b,phi))near(M.quad(S,pt),1);
}
near(M.model('normal',1).info,1);near(M.model('normal',5).info,.04);
const S=[[4,3],[3,4]],I=M.inv(S);near(I[0][0],4/7);near(I[0][1],-3/7);
console.log('PASS: analytic score/Hessian vs finite differences; covariance inverses; ellipse geometry; lecture endpoints.');
