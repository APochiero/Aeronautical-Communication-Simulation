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

simple Transmitter
{
    parameters:
       // TODO
       int nBS;  
   
       @signal[computeServiceTime](type="simtime_t");
       @statistic[serviceTime](source="computeServiceTime"; record=vector;);

       @signal[computeQueueLength](type="long");
       @statistic[queueLength](source="computeQueueLength"; record=vector;);

       @signal[computeDistance](type="long");
       @statistic[distance](source="computeDistance"; record=vector;);
       
       @signal[computeResponseTime](type="double");
       @statistic[responseTime](source="computeResponseTime"; record=vector;);

       @signal[computeWaitingTime](type="double");
       @statistic[waitingTime](source="computeWaitingTime"; record=vector;);

       @signal[serviceTimeBeforeHandover](type="double");
       @statistic[serviceTimeBeforeHandover](source="serviceTimeBeforeHandover"; record=vector;);

       @signal[serviceTimeAfterHandover](type="double");
       @statistic[serviceTimeAfterHandover](source="serviceTimeAfterHandover"; record=vector;);

       @signal[arrival](type="double");
       @statistic[interarrivalTime](source="arrival"; record=vector;);
    gates:
        output out[nBS];
}
