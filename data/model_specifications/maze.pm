// maze example (POMDP) as an MDP
// slightly extends that presented in
// Littman, Cassandra and Kaelbling
// Learning policies for partially observable environments: Scaling up
// Technical Report CS, Brown University
// gxn 29/01/16
// Made into a MDP for documentation of stormpy.

// state space (value of variable "s")

//  0  1  2  3  4
//  5     6     7
//  8     9    10
// 11     13   12

// 13 is the target

mdp


module maze

	s : [-1..13];

	// initialisation
	[] s=-1 -> 1/13 : (s'=0)
			 + 1/13 : (s'=1)
			 + 1/13 : (s'=2)
			 + 1/13 : (s'=3)
			 + 1/13 : (s'=4)
			 + 1/13 : (s'=5)
			 + 1/13 : (s'=6)
			 + 1/13 : (s'=7)
			 + 1/13 : (s'=8)
			 + 1/13 : (s'=9)
			 + 1/13 : (s'=10)
			 + 1/13 : (s'=11)
			 + 1/13 : (s'=12);

	// moving around the maze

	[east] s=0 -> (s'=1);
	[west] s=0 -> (s'=0);
	[north] s=0 -> (s'=0);
	[south] s=0 -> (s'=5);

	[east] s=1 -> (s'=2);
	[west] s=1 -> (s'=0);
	[north] s=1 -> (s'=1);
	[south] s=1 -> (s'=1);

	[east] s=2 -> (s'=3);
	[west] s=2 -> (s'=1);
	[north] s=2 -> (s'=2);
	[south] s=2 -> (s'=6);

	[east] s=3 -> (s'=4);
	[west] s=3 -> (s'=2);
	[north] s=3 -> (s'=3);
	[south] s=3 -> (s'=3);

	[east] s=4 -> (s'=4);
	[west] s=4 -> (s'=3);
	[north] s=4 -> (s'=4);
	[south] s=4 -> (s'=7);

	[east] s=5 -> (s'=5);
	[west] s=5 -> (s'=5);
	[north] s=5 -> (s'=0);
	[south] s=5 -> (s'=8);

	[east] s=6 -> (s'=6);
	[west] s=6 -> (s'=6);
	[north] s=6 -> (s'=2);
	[south] s=6 -> (s'=9);

	[east] s=7 -> (s'=7);
	[west] s=7 -> (s'=7);
	[north] s=7 -> (s'=4);
	[south] s=7 -> (s'=10);

	[east] s=8 -> (s'=8);
	[west] s=8 -> (s'=8);
	[north] s=8 -> (s'=5);
	[south] s=8 -> (s'=11);

	[east] s=9 -> (s'=9);
	[west] s=9 -> (s'=9);
	[north] s=9 -> (s'=6);
	[south] s=9 -> (s'=13);

	[east] s=10 -> (s'=10);
	[west] s=10 -> (s'=10);
	[north] s=10 -> (s'=7);
	[south] s=10 -> (s'=12);

	[east] s=11 -> (s'=11);
	[west] s=11 -> (s'=11);
	[north] s=11 -> (s'=8);
	[south] s=11 -> (s'=11);

	[east] s=12 -> (s'=12);
	[west] s=12 -> (s'=12);
	[north] s=12 -> (s'=10);
	[south] s=12 -> (s'=12);

	// loop when we reach the target
	[done] s=13 -> true;

endmodule

// reward structure (number of steps to reach the target)
rewards

	[east] true : 1;
	[west] true : 1;
	[north] true : 1;
	[south] true : 1;

endrewards

// target observation
label "goal" = s=13;