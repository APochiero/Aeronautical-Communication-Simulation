//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package barsimulator;

module Kitchen
{
    parameters:
        double T = default(3);
        int policy = default(1);
    gates:
        input in;
		output out;
    submodules:
        owner: Owner;
        chef1: Chef;
        chef2: Chef;
    connections:
        // in to owner
        in --> {delay = 100ms;} --> owner.in[2];
        
        // owner to chefs
        chef1.in <-- {delay = 100ms;} <-- owner.out[0]; 
        chef2.in <-- {delay = 100ms;} <-- owner.out[1]; 
        
        // chefs to owner 
        chef1.out --> {delay = 100ms;} --> owner.in[0];
        chef2.out --> {delay = 100ms;} --> owner.in[1];
        
		// onwer to out 
        out <-- { delay = 100ms; } <-- owner.out[2];    
}
