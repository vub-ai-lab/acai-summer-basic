classdef Ice2 < Ice
    % Ice MDP environment.
    % Introduces transition probabilities
    %
    % All methods necessary to apply Value Iteration are implemented in
    % this class and its superclass 'Ice'.
    %
    % Methods:
    %   * Create an environment:
    %       env = Ice2(gamma);
    %   * Get probability of transition:
    %       probability = env.transition_probability(state, action,
    %       next_state);
    %
    % Inherited:
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
    
    properties(Access = 'private')
        PROB_MATRIX = []; % Transition probability matrix
    end
    
    methods
        function obj = Ice2(gamma, slip_prob)
            % Constructor.
            %
            % INPUT:
            %   * gamma (float): discount factor
            %   * slip_prob (float): slipping probability per status (optional: default = 0.05)
            
            if nargin < 2
                slip_prob = 0.05;
            end
            obj = obj@Ice(gamma, slip_prob);
            obj = obj.compute_transition_matrix();
        end
        
        function p = transition_probability(obj, state, action, next_state)
            % Get the transition probability for a given state transition.
            %
            % INPUT:
            %   * state (1 x 2 vector)
            %   * action (integer)
            %   * next_state (1 x 2 vector)
            % OUTPUT:
            %   * p (float): Transition probability
            
            p = obj.PROB_MATRIX(state(1), state(2), action, next_state(1), next_state(2));
        end
    end
    
    methods(Access = 'private')
        function obj = compute_transition_matrix(obj)
            % Compute transition probability matrix.
            
            [dim_s1, dim_s2] = size(obj.WORLD);
            dim_a = size(obj.ACTIONS, 1);
            obj.PROB_MATRIX = zeros(dim_s1, dim_s2, dim_a, dim_s1, dim_s2);

            for s1 = 1:dim_s1
                for s2 = 1:dim_s2
                    if ~obj.is_terminal([s1, s2])
                        for a = 1:dim_a
                            for slip = 0:1
                                if logical(slip)
                                    prob = obj.SLIP_PROB;
                                else
                                    prob = 1 - obj.SLIP_PROB;
                                end
                                next_state = obj.compute_next_state([s1 s2], a, logical(slip));
                                transition = {s1, s2, a, next_state(1), next_state(2)};
                                obj.PROB_MATRIX(transition{:}) = obj.PROB_MATRIX(transition{:}) + prob;
                            end
                        end
                    end
                end
            end
        end
    end
end
