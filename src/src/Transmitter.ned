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
       int nBS;
       @signal[packetSent](type="double");
       @statistic[serviceTime](source="packetSent"; record=vector;);

       @signal[newPacket](type="long");
       @statistic[queueLength](source="newPacket"; record=vector;);

       @signal[handover](type="long");
       @statistic[nHandover](source="handover"; record=vector;);

       @signal[avoidHandover](type="long");
       @statistic[nAvoidedHandover](source="avoidHandover"; record=vector;);

       @signal[distance](type="long");
       @statistic[distance](source="distance"; record=vector;);
       
       @signal[handoverDone](type="long");
       @statistic[handoverDone](source="handoverDone"; record=vector;);
       
       @signal[handover](type="long");
       @statistic[handover](source="handover"; record=vector;);

       @signal[computeResponseTime](type="double");
       @statistic[responseTime](source="computeResponseTime"; record=vector;);

       @signal[computeWaitingTime](type="double");
       @statistic[waitingTime](source="computeWaitingTime"; record=vector;);

       @signal[serviceTimeBeforeHandover](type="double");
       @statistic[serviceTimeBeforeHandover](source="serviceTimeBeforeHandover"; record=vector;);

       @signal[serviceTimeAfterHandover](type="double");
       @statistic[serviceTimeAfterHandover](source="serviceTimeAfterHandover"; record=vector;);

    gates:
        output out[nBS];
}
