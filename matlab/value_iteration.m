% Parameters
N_ITERATIONS = 200;
GAMMA = 0.9;

% Create environment
env = Ice2(GAMMA);

% Run VI
V_prev = zeros(4, 4);
for k = 1:N_ITERATIONS
    disp(['iteration ', int2str(k)]);
    V = zeros(4, 4);
	for s1 = 1:4
    	for s2 = 1:4
            % Per state s = [s1, s2], compute V(s) by taking the maximum Q(s,a).
            vals = zeros(1, 4);
        	for a = 1:4
                % Compute Q(s, a)
            	for next_s1 = 1:4
                	for next_s2 = 1:4
                        % Iterate over possible transitions, compute
                        % R(s, a, s') + GAMMA*V(s') for all next state values V(s'),
                        % and weigh them with their probability of occurrence.
                    	p = env.transition_probability([s1, s2], a, [next_s1, next_s2]);
                    	val = env.reward([s1, s2], a, [next_s1, next_s2]) + GAMMA * V_prev(next_s1, next_s2);
                    	vals(a) = vals(a) + p * val;
                	end
            	end
        	end
            V(s1, s2) = max(vals);
    	end
	end
    V_prev = V;
end

% Compute policy from values.
policy = zeros(4, 4);
for s1 = 1:4
    for s2 = 1:4
        % Per state s = [s1 s2], the optimal action is the one with the
        % highest expected long-term reward.
        vals = zeros(1, 4);
        for a = 1:4
            for next_s1 = 1:4
                for next_s2 = 1:4
                    p = env.transition_probability([s1, s2], a, [next_s1, next_s2]);
                    val = env.reward([s1, s2], a, [next_s1, next_s2]) + GAMMA * V(next_s1, next_s2);
                    vals(a) = vals(a) + p * val;
                end
            end
        end
        [~, policy(s1, s2)] = max(vals);
    end
end