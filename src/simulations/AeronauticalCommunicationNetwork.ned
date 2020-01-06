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
        @display("bgb=72802.914,21000.84,white");
    //        @display("bgb=25000,25000,white;");
    submodules:
        aircraft[nAircrafts]: Aircraft {
            @display("p=18200.729,11600.464");
        }
        bs[nBS]: BaseStation {
            @display("i=device/antennatower_s;p=36201.445,11600.464");
            //	    	@display("p=12500, 12500");   
            @display("p=12500,12500,m,4,25000,25000");
        }
        controlTower: ControlTower { // utile per collezionare statistiche sull'intero sistema
            @display("i=device/mainframe;p=54202.168,11600.464");
        }
        visualizer: IntegratedVisualizer {
            parameters:
                @display("p=6200.248,3200.128");
        }

    connections:
        for i=0..nAircrafts-1, for j=0..nBS-1 {
            aircraft[i].out[j] --> { @display("ls=,0"); } --> bs[j].in[i];
        }
        for i=0..nBS-1 {
            bs[i].out --> controlTower.in[i];
        }
}
