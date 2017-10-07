% Parameters
EPISODES = 60000;
EPSILON = 0.1;
GAMMA = 0.9;
ALPHA = 0.1;

% Create environment
env = Ice(GAMMA);

% Run
all_cumulative_rewards = zeros(1, EPISODES);
Q = zeros(4, 4, length(env.actions()));
for e = 1:EPISODES
    % Start episode
    total_reward = 0;
    s = env.start_state();
    done = false;
    while ~done
        % Select action
        [~, greedy] = max(Q(s(1), s(2), :));
        if rand() < EPSILON
            a = randi([1, length(env.actions())]);
        else
            a = greedy;
        end
    
        % Apply action and compute reward.
        next_s = env.transition(s, a);
        r = env.reward(s, a, next_s);
        done = env.is_terminal(next_s);
    
        % Update Q-table
        if done
            max_next_Q = 0;
        else
            max_next_Q = max(Q(next_s(1), next_s(2), :));
        end
        td = r + GAMMA*max_next_Q - Q(s(1), s(2), a);
        Q(s(1), s(2), a) = Q(s(1), s(2), a) + ALPHA*td;
    
        % Go to next state
        s = next_s;

        total_reward = total_reward + r;
    end
    
    % Output episode statistics
    disp(['Episode ', int2str(e), ': reward = ', int2str(total_reward)])
    
    if e - 1 == 0
        all_cumulative_rewards(e) = total_reward;
    else
        all_cumulative_rewards(e) = 0.95*all_cumulative_rewards(e-1) + 0.05*total_reward;
    end
end
plot(1:EPISODES, all_cumulative_rewards);