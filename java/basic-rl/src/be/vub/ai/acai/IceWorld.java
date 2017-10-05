package be.vub.ai.acai;

public class IceWorld {
	protected final double slipProb = 0.05;
	
	protected enum Cell {
		E (0),   //Empty
		P (-10),  //Pit
		T (20),  //Treasure
		G (100); //Goal
		
		protected final int reward;
		Cell(int reward) {
			this.reward = reward;
		}
	}
	
	public enum Action {
		Up,
		Down,
		Left,
		Right;
	}
	
	private int x, y;
	protected static Cell[][] grid = {
			{Cell.E, Cell.E, Cell.E, Cell.G},
			{Cell.E, Cell.P, Cell.E, Cell.P},
			{Cell.E, Cell.E, Cell.T, Cell.P},
			{Cell.E, Cell.P, Cell.P, Cell.P},
		};

	
	//Put the agent in the bottom-left corner of the environment
	public IceWorld() {
		this.x = 0;
		this.y = 3;
	}
	
	public static class State {
		int x;
		int y;
		public State(int x, int y) {
			this.x = x;
			this.y = y;
		}
	}
	public State getCurrentState() {
		return new State(x, y);
	}
	
	public static boolean isFinalState(State s) {
		Cell c =grid[s.y][s.x];
		return c == Cell.G | c == Cell.P;
	}
	
	public double step(Action a) {
		int slipX = this.x;
		int slipY = this.y;
		switch (a) {
			case Up:
				if (this.y > 0) {
					this.y -= 1;
					slipY = 0;
				}
				break;				
			case Down:
				if (this.y < 3) {
					this.y += 1;
					slipY = 3;
				}
				break;
			case Left:
				if (this.x > 0) {
					this.x -= 1;
					slipX = 0;
				}
				break;
			case Right:
				if (this.x < 3) {
					this.x += 1;
					slipX = 3;
				}
				break;
		}
		
		if (Math.random() < slipProb) {
			this.x = slipX;
			this.y = slipY;
		}
		
		return grid[this.y][this.x].reward;
	}
	
}
