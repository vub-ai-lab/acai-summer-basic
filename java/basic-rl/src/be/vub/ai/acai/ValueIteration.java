package be.vub.ai.acai;

import java.util.Arrays;
import be.vub.ai.acai.IceWorld.Action;
import be.vub.ai.acai.IceWorld.State;

public class ValueIteration {

	//array with a value for each state
	double[][] values;
	private IceWorld2 env;
	static final int iterations = 10000;
	static final double gamma = 0.9;
	
	public ValueIteration() {
		values = new double[4][4];
		env = new IceWorld2();
	}

	private static double[][] deepCopy(double[][] original) {
	    if (original == null) {
	        return null;
	    }
	    final double[][] result = new double[original.length][];
	    for (int i = 0; i < original.length; i++) {
	        result[i] = Arrays.copyOf(original[i], original[i].length);
	    }
	    return result;
	}
	
	private double bestValue(double [] values) {
		double maxValue = values[0];
		for (int i = 1; i < values.length; i++) {
			if (values[i] > maxValue) {
				maxValue = values[i];
			}
		}
		return maxValue;
	}
	
	public void printValues(){
		for (int i=0; i < values[0].length; ++i) {
		    System.out.println(Arrays.toString(values[i]));
		}
	}

	public void run() {
		final int gridDim = 4;
		double [][] prev_values = deepCopy(values);
		for(int i=0;i<ValueIteration.iterations;i++){
			for (int x=0;x<gridDim;x++){
				for (int y=0;y<gridDim;y++){
					double [] Qvals = new double[IceWorld.Action.values().length];
					for (Action a:IceWorld.Action.values()){
						for (int nextX=0;nextX<gridDim;nextX++){
							for (int nextY=0;nextY<gridDim;nextY++){
								State s1 = new State(x, y);
								State s2 = new State(nextX, nextY);
								double prob = this.env.transition_probability(s1, a, s2);
								double reward = this.env.get_reward(s1, a, s2);
								Qvals[a.ordinal()] += prob * (reward + gamma * prev_values[nextY][nextX]); 
							}
						}
					}
					this.values[y][x] = bestValue(Qvals);
				}
			}
			prev_values = deepCopy(this.values);
		}
	}
	
	public static void main(String [] args) {
		ValueIteration VI = new ValueIteration();
		VI.run();
		VI.printValues();
	}
}
