classdef Ice
    % Ice MDP environment.
    %
    % All methods necessary to apply Q-learning are implemented in
    % this class.
    %
    % Methods:
    %   * Create an environment:
    %       env = Ice(gamma);
    %   * Get possible actions:
    %       actions = env.actions();
    %   * Get starting state:
    %       state = env.start_state();
    %   * Get discount factor:
    %       gamma = env.discount_factor();
    %   * Check whether given state is terminal:
    %       terminal = env.is_terminal(state);
    %   * Retrieve reward for transition:
    %       reward = env.reward(state, action, next_state);
    %   * Apply transition:
    %       next_state = env.transition(state, action);

    properties(Access='protected')
        GAMMA = 0;
        SLIP_PROB = 0;
        WORLD = [1 1 1 4;
                 1 2 1 2;
                 1 1 3 2;
                 1 2 2 2]; % 0 - ice, 1 - cracked ice, 2 - treasure, 3 - goal
        DIMENSIONS = [4 4];
        ACTIONS = [-1  0; % up
                    1  0; % down
                    0 -1; % left
                    0  1] % right
        START = [4 1];
        REWARD = [0 -10 20 100]; % rewards for encountered cell in world
        TERMINAL = logical([0, 1, 0, 1]) % true if encountered cell in world is terminal
    end

    methods
        function obj = Ice(gamma, slip_prob)
            % Constructor.
            %
            % INPUT:
            %   * gamma (float): discount factor
            %   * slip_prob (float): slipping probability per status (optional: default = 0.05)
            
            obj.GAMMA = gamma;
            if nargin == 2
                obj.SLIP_PROB = slip_prob;
            else
                obj.SLIP_PROB = 0.05;
            end
        end
        
        function state = start_state(obj)
            % Get start state
            
            state = obj.START;
        end
        
        function A = actions(obj)
            % Return action indices

            A = 1:size(obj.ACTIONS, 1);
        end
        
        function gamma = discount_factor(obj)
            gamma = obj.GAMMA;
        end
        
        function done = is_terminal(obj, state)
            % True if the given state is 1 or 3 in the world.
            %
            % INPUT:
            %   * state (1 x 2 vector)
            % OUTPUT:
            %   * done (boolean): True if the given state is terminal.

            status = obj.WORLD(state(1), state(2));
            done = obj.TERMINAL(status);
        end
        
        function r = reward(obj, ~, ~, next_state)
            % Reward depending on the status in the world.
            %     status | reward
            %     ---------------
            %          0 |      0
            %        -10 |      1
            %         20 |      2
            %        100 |      3
            %
            % INPUT:
            %   * state (1 x 2 vector)
            %   * action (integer)
            %   * next_state (1 x 2 vector)
            % OUTPUT:
            %   * r (float): Reward for transition
     
            status = obj.WORLD(next_state(1), next_state(2));
            r = obj.REWARD(status);
        end
        
        function next_state = transition(obj, state, action)
            % Apply an action to the current state and perform a transition
            % into another state.
            %
            % INPUT:
            %   * state (1 x 2 vector)
            %   * action (integer)
            % OUTPUT:
            %   * next_state (1 x 2 vector)
            
            % Apply transition
            slip = rand() < obj.SLIP_PROB; % Slipped?
            next_state = obj.compute_next_state(state, action, slip);
        end
    end

    methods(Access = 'protected')
        function next_state = compute_next_state(obj, state, action, slip)
            % Apply an action to a given state and compute the next state.
            %
            % INPUT:
            %   * state (1 x 2 vector)
            %   * action (integer)
            %   * slip (boolean): True if the agent slipped.
            % OUTPUT:
            %   * next_state (1 x 2 vector)
            
            % Apply transition.
            transition = obj.ACTIONS(action,:);
            if slip
                transition = transition .* size(obj.WORLD); % Overshoot action
            end
            next_state = state + transition;
            
            % Resolve out of bounds cases.
            if next_state(1) < 1
                next_state(1) = 1;
            elseif next_state(1) > size(obj.WORLD, 1)
                next_state(1) = size(obj.WORLD, 1);
            end
            if next_state(2) < 1
                next_state(2) = 1;
            elseif next_state(2) > size(obj.WORLD, 2)
                next_state(2) = size(obj.WORLD, 2);
            end
        end
    end
end