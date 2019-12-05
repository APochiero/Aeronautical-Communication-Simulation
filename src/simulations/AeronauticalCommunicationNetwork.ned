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

package aeronauticalcommunicationsimulator.simulations;

import aeronauticalcommunicationsimulator.Aircraft; 
import aeronauticalcommunicationsimulator.ControlTower; 
import aeronauticalcommunicationsimulator.BaseStation; 


import inet.visualizer.integrated.IntegratedVisualizer;
import inet.visualizer.scene.SceneVisualizer;

network AeronauticalCommunicationNetwork
{
    parameters:
        int nAircrafts;
        int nBS;
        string interarrivalDistribution = default("exponential");
        @display("bgb=25000,25000,white;");
    submodules:
        aircraft[nAircrafts]: Aircraft;
        bs[nBS]: BaseStation {
	    	@display("i=device/antennatower_s");    
//	    	@display("p=12500,12500,m,4,25000,25000");      
        };
        controlTower: ControlTower { // utile per collezionare statistiche sull'intero sistema
	    	@display("i=device/mainframe");   
        };         
        visualizer: IntegratedVisualizer {
            parameters:
                @display("p=100,50");
        }
      
     connections:
         for i=0..nAircrafts-1, for j=0..nBS-1 {
    		aircraft[i].out[j] --> {@display("ls=,0");} -->  bs[j].in[i];
//    		aircraft[i].out[j] -->  bs[j].in[i];
         }
         for i=0..nBS-1 {
         	bs[i].out --> controlTower.in[i];
         }
}