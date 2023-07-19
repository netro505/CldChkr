mdp

const int N;

const double p;
const double q;

formula grass = (x = 3 | y = 4);

module main
   x : [1..N] init 1;
   y : [1..N] init 3;

   [north] x > 1 -> p:(x'=max(x-1,1)) + (1-p):(x'=max(x-2,1));
   [south] x < N -> p:(x'=min(x+1,N)) + (1-p):(x'=min(x+2,N));
   [west] y > 1 -> q:(y'=max(y-1,1)) + (1-q):(y'=max(y+1,1));
   [east] y < N -> q:(y'=min(y+1,N)) + (1-q):(y'=min(y+1,N));
endmodule

formula station1 = x=3 & y=1;
formula station2 = x=1 & y=1;
label "station" = station1 | station2;
label "castle" = x=N & y=N;

rewards "movecost"
    grass: 2;
    !grass: 1; 
endrewards

rewards "xdominated"
    true : x;
endrewards