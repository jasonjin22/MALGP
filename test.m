function [mean1, mean2] = test(X1, X2, y, param, Test1, Test2)
    meanfunc1 = @meanZero; 
    likfunc1 = @likGauss; 
    covfunc1 = @covSEiso;
    hyp1.cov = [param(1),param(2)];
    hyp1.mean = [];    
    hyp1.lik = param(3);

    meanfunc2 = @meanZero; 
    likfunc2 = @likGauss; 
    covfunc2 = @covSEiso;
    hyp2.cov = [param(4),param(5)];
    hyp2.mean = []; 
    hyp2.lik = param(6);
    
    [mean1, var1] = gp(hyp1, @infExact, meanfunc1, covfunc1, likfunc1, X1, y, Test1);
    [mean2, var2] = gp(hyp2, @infExact, meanfunc2, covfunc2, likfunc2, X2, y, Test2);   
    
end
