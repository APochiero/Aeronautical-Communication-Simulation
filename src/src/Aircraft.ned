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

package aeronauticalcommunicationsimulator;
import inet.mobility.contract.IMobility;

module Aircraft
{
    parameters:
        // TODO
	   	@display("i=device/cellphone_s");
	   	int nBS;
    	int rows;
    	int cols;
    	int M;
    	double t @unit(s);
    	double k @unit(s);
    	double T;
    	double p @unit(s); 
	gates:
	    output out[nBS];
    submodules:
        mobility: <> like IMobility;
        transmitter: Transmitter;
    connections:
    	for i=0..nBS-1 {
    		transmitter.out[i] --> out[i];
    	}
}
