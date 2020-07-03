function [J, grad] = objFunction(pa, X1, X2, y, a, b)
    hyp1.cov = [pa(1),pa(2)];
    hyp1.lik = pa(3); 
    sigma2 = exp(2*pa(3));  % sigma.^2
    hyp2.cov = [pa(4),pa(5)];
    hyp2.lik = pa(6); 
    beta2 = exp(2*pa(6));  %beta.^2
    n=size(X1,1);
    x1=X1;
    x2=X2;

    K1=covSEiso(hyp1.cov,x1);
    K2=covSEiso(hyp2.cov,x2);
    K1=(K1+K1')/2;  
    K2=(K2+K2')/2;
    C1=K1+(sigma2)*eye(n);
    C2=K2+(beta2)*eye(n); 
    C1=(C1+C1')/2;
    [v,l]= eig(C1);
% 将原来的存有特征值的方阵l中小于eps的特征值换成eps
    ll  = l;
    eps = 10^-10;
    ll(find(ll<eps))=eps;
    ll = diag(diag(ll));
    KK = v*ll*v'+eye(n)*eps;
    dd= det(KK);
    while dd==0
        [v,l]= eig(C1);
        ll  = l;
        eps = eps*10;
        ll(find(ll<eps))=eps;
        ll = diag(diag(ll));
        KK = v*ll*v'+eye(n)*eps;
        dd= det(KK);
    end
    % c是一个上三角矩阵
    c = chol(KK);
    inC1 = inv(c)*inv(c)';
    lndetC1=2 * sum(log(diag(c))); 

    C2=(C2+C2')/2;
    [v,l]= eig(C2);
    ll  = l;
    eps = 10^-10;
    ll(find(ll<eps))=eps;
    ll = diag(diag(ll));
    KK = v*ll*v'+eye(n)*eps;
    dd= det(KK);
    while dd==0
        [v,l]= eig(C2);
        ll  = l;
        eps = eps*10;
        ll(find(ll<eps))=eps;
        ll = diag(diag(ll));
        KK = v*ll*v'+eye(n)*eps;
        dd= det(KK);
    end
    c = chol(KK);
    inC2 = inv(c)*inv(c)';
    lndetC2=2 * sum(log(diag(c)));
    
    A1=K1*(eye(n)-inC1*K1); % Sigma_1
    A2=K2*(eye(n)-inC2*K2); % Sigma_2
%     size(K1)
%     size(inC1)
%     size(y)
    mu1=K1*(inC1)*y;
    mu2=K2*(inC2)*y;

    A1=(A1+A1')/2;
    [v,l]= eig(A1);
    ll  = l;
    eps = 10^-10;
    ll(find(ll<eps))=eps;
    ll = diag(diag(ll));
    KK = v*ll*v'+eye(n)*eps;
    dd= det(KK);
    while dd==0
        [v,l]= eig(A1);
        ll  = l;
        eps = eps*10;
        ll(find(ll<eps))=eps;
        ll = diag(diag(ll));
        KK = v*ll*v'+eye(n)*eps;
        dd= det(KK);
    end
    c = chol(KK);
    inA1 = inv(c)*inv(c)';

    A2=(A2+A2')/2;
    [v,l]= eig(A2);
    ll  = l;
    eps = 10^-10;
    ll(find(ll<eps))=eps;
    ll = diag(diag(ll));
    KK = v*ll*v'+eye(n)*eps;
    dd= det(KK);
    while dd==0
        [v,l]= eig(A2);
        ll  = l;
        eps = eps*10;
        ll(find(ll<eps))=eps;
        ll = diag(diag(ll));
        KK = v*ll*v'+eye(n)*eps;
        dd= det(KK);
    end
    c = chol(KK);
    inA2 = inv(c)*inv(c)';

    part1=a/2*((y'*(inC1)*y)+lndetC1);
    part2=(1-a)/2*((y'*(inC2)*y)+lndetC2);
    temp1=trace((inA2)*A1)+(mu2-mu1)'*(inA2)*(mu2-mu1);
    temp2=trace((inA1)*A2)+(mu1-mu2)'*(inA1)*(mu1-mu2);
    part3=b/2*(temp1+temp2-2*n);
    J=part1+part2+part3;
    
    
    gd_K1_th1=covSEiso(hyp1.cov,x1,[],1);
    gd_K1_th2=covSEiso(hyp1.cov,x1,[],2);
    gd_K1_s={gd_K1_th1,gd_K1_th2,zeros(n)};
    gd_C1_s={gd_K1_th1,gd_K1_th2,2*sigma2*eye(n)};
    gd_1={0,0,0};
    gd_K2_th3=covSEiso(hyp2.cov,x2,[],1);
    gd_K2_th4=covSEiso(hyp2.cov,x2,[],2);
    gd_K2_s={gd_K2_th3,gd_K2_th4,zeros(n)};
    gd_C2_s={gd_K2_th3,gd_K2_th4,2*beta2*eye(n)};
    gd_2={0,0,0};

    for i=1:3       
%        disp(i)
       gd_K1=gd_K1_s{i};
       gd_C1=gd_C1_s{i};
       gd_inC1=-(inC1)*gd_C1*(inC1);
       gd_A1=gd_K1-(...
           gd_K1*(inC1)*K1+K1*gd_inC1*K1+K1*(inC1)*gd_K1);
       gd_inA1=-(inA1)*gd_A1*(inA1);
       gd_mu1=(gd_K1*(inC1)+K1*gd_inC1)*y;
%        disp(gd_inC1(351, 351))
%        disp(gd_A1(351, 351))
%        disp(gd_inA1(351, 351))
%        disp(gd_mu1(351))
        part1=a/2*(trace((inC1)*gd_C1)+...
        y'*gd_inC1*y);
        temp1=trace((inA2)*gd_A1)+...
        (-gd_mu1)'*(inA2)*(mu2-mu1)+...
        (mu2-mu1)'*(inA2)*(-gd_mu1);

        temp2=trace(gd_inA1*A2)+...
        (gd_mu1)'*(inA1)*(mu1-mu2)+...
        (mu1-mu2)'*gd_inA1*(mu1-mu2)+...
        (mu1-mu2)'*(inA1)*gd_mu1;
        part2=b/2*(temp1+temp2);
        %       disp("gd1 temp1:")
        %       disp(temp1)
        %       disp("gd1 temp2:")
        %       disp(trace(gd_inA1*A2))
        %       disp((gd_mu1)'*(inA1)*(mu1-mu2))
        %       disp((mu1-mu2)'*gd_inA1*(mu1-mu2))
        %       disp((mu1-mu2)'*(inA1)*gd_mu1)
        gd_1{i}=part1+part2;


        gd_K2=gd_K2_s{i};
        gd_C2=gd_C2_s{i};
        gd_inC2=-(inC2)*gd_C2*(inC2);
        gd_A2=gd_K2-(...
           gd_K2*(inC2)*K2+K2*gd_inC2*K2+K2*(inC2)*gd_K2);
        gd_inA2=-(inA2)*gd_A2*(inA2);
        gd_mu2=(gd_K2*(inC2)+K2*gd_inC2)*y;
          part1=(1-a)/2*(trace((inC2)*gd_C2)+...
              y'*gd_inC2*y);
          temp1=trace(gd_inA2*A1)+...
              (gd_mu2)'*(inA2)*(mu2-mu1)+...
              (mu2-mu1)'*gd_inA2*(mu2-mu1)+...
              (mu2-mu1)'*(inA2)*gd_mu2;
          temp2=trace((inA1)*gd_A2)+...
              (-gd_mu2)'*(inA1)*(mu1-mu2)+...
              (mu1-mu2)'*(inA1)*(-gd_mu2);
          part2=b/2*(temp1+temp2);
        %       disp("gd2 temp1:")
        %       disp(temp1)
        %       disp("gd2 temp2:")
        %       disp(temp2)
          gd_2{i}=part1+part2;
    end
    grad_th1=gd_1{1};
    grad_th2=gd_1{2};
    grad_sigma=gd_1{3};

    grad_th3=gd_2{1};
    grad_th4=gd_2{2};
    grad_beta=gd_2{3};
    grad=[grad_th1 grad_th2 grad_sigma grad_th3 grad_th4 grad_beta];
end
