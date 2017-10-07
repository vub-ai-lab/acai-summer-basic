package be.vub.ai.acai;


public class QLearning {
	static class QValues {
		//array with a value for each action
		double[] values = new double[4];
		
		static class QValue {
			public QValue(IceWorld.Action action, double value) {
				this.action = action;
				this.value = value;
			}
			public IceWorld.Action action;
			public double value;
		}
		
		QValue bestQValue() {
			int maxIndex = 0;
			double maxValue = values[0];
			for (int i = 1; i < 4; i++) {
				if (values[i] > maxValue) {
					maxValue = values[i];
					maxIndex = i;
				}
			}
			return new QValue(IceWorld.Action.values()[maxIndex], maxValue);
		}
		
		double getValue(IceWorld.Action action) {
			return values[action.ordinal()];
		}
		
		void setValue(IceWorld.Action action, double value) {
			values[action.ordinal()] = value;
		}
	}
	
	static int randInRange(int min, int max) {
		return (int)(Math.random() * ((max - min) + 1)) + min;
	}
	
	static final int episodes = 10000;
	static final double epsilon = 0.1;
	static final double gamma = 0.9;
	static final double	learningRate = 0.1;
	
	public static void run() {
		final int nrStates = 4;
		QValues[][] qtable = new QValues[nrStates][nrStates];
		for (int i = 0; i < nrStates; i++) {
			for (int j = 0; j < nrStates; j++) {
				qtable[i][j] = new QValues();
			}
		}
		
		System.out.println("episode,cumulative_reward");

		for (int i = 0; i < episodes; i++) {
			double cumulativeReward = runEpisode(new IceWorld(), qtable);
			System.out.println((i+1) + "," + cumulativeReward);
		}
	}
	
	public static double runEpisode(IceWorld env, QValues[][] qtable) {
		double cumulativeReward = 0.0;
		
		boolean terminate = false;
		while (!terminate) {
			//Compute what the greedy action for the current state is
			IceWorld.State state = env.getCurrentState();
			IceWorld.Action greedyAction = 
					qtable[state.x][state.y].bestQValue().action;
			
			//Sometimes, the agent takes a random action, 
			//to explore the environment
			IceWorld.Action action = null;
			if (Math.random() < epsilon) 
				action = IceWorld.Action.values()[randInRange(0, 3)];
			else
				action = greedyAction;
			
			//Perform the action
			double reward = env.step(action);
			IceWorld.State nextState = env.getCurrentState();
			if (IceWorld.isFinalState(nextState)) 
				terminate = true;
			
			//Update the q-table
			double qDiff = 
				qtable[nextState.x][nextState.y].bestQValue().value -
				qtable[state.x][state.y].getValue(action);
			double tdError = reward + (gamma * qDiff);
			qtable[state.x][state.y].setValue(action, learningRate * tdError);

			//Update the cumulative reward
			cumulativeReward += reward;
		}
		
		return cumulativeReward;
	}
	
	public static void main(String [] args) {
		QLearning.run();
	}
}
