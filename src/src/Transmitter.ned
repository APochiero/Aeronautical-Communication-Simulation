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
       @signal[computeServiceTime](type="double");
       @signal[computeResponseTime](type="double");
       @signal[computeWaitingTime](type="double");      
       @signal[computeQueueLength](type="long");
       @signal[handover](type="long");
	   @signal[handoverDone](type="long");
       @signal[computeDistance](type="long");
       
       @statistic[serviceTime](source="computeServiceTime"; record=vector;); 
       @statistic[queueLength](source="computeQueueLength"; record=vector;);
       @statistic[handover](source="handover"; record=vector;);
       @statistic[handoverDone](source="handoverDone"; record=vector;);
       @statistic[distance](source="computeDistance"; record=vector;);
       @statistic[responseTime](source="computeResponseTime"; record=vector;);
       @statistic[waitingTime](source="computeWaitingTime"; record=vector;);

    gates:
        output out[nBS];
}
