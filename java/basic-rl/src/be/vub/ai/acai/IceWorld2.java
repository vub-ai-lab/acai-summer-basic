package be.vub.ai.acai;

public class IceWorld2 extends IceWorld {

	public IceWorld2() {
		super();
	}
	
	public double transition_probability(State s1, Action a, State s2) {
		int nextX = s1.x;
		int nextY = s1.y;
		int slipX = s1.x;
		int slipY = s1.y;
		if(isFinalState(s1)){
			return 0;
		}
		switch (a) {
			case Up:
				if (s1.y > 0) {
					nextY -= 1;
					slipY = 0;
				}
				break;				
			case Down:
				if (s1.y < 3) {
					nextY += 1;
					slipY = 3;
				}
				break;
			case Left:
				if (s1.x > 0) {
					nextX -= 1;
					slipX = 0;
				}
				break;
			case Right:
				if (s1.x < 3) {
					nextX += 1;
					slipX = 3;
				}
				break;
		}
		double prob = 0;
		if (s2.x == nextX && s2.y == nextY){
			prob += 1 - this.slipProb;
		}

		if (s2.x == slipX && s2.y == slipY){
			prob += this.slipProb;
		}
		
		return prob;
	}
	
	public double get_reward(State s1, Action a, State s2) {
		return IceWorld2.grid[s2.y][s2.x].reward;
	}

}
