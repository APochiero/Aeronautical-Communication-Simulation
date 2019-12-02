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

//
// TODO auto-generated module
//
simple Transmitter
{
    parameters:
       // TODO
       int nBS;  
       @signal[packetSent](type="double");
       @signal[newPacket](type="int");
       @signal[handover](type="int");
       @signal[avoidHandover](type="int");
       
       @statistic[serviceTime](source="packetSent"; record=vector;); 
       @statistic[queueLength](source="newPacket"; record=vector;);
       @statistic[nHandover](source="handover"; record=sum;);
       @statistic[nAvoidedHandover](source="avoidHandover"; record=sum;);
       
    gates:
        output out[nBS];
}
