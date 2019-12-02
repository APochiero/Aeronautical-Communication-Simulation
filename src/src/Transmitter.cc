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

#include "Transmitter.h"
#include <string>
#include "AircraftPacket_m.h"

using namespace inet;
using namespace std;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize()
{

    nBS = par("nBS").intValue();
    k = getAncestorPar("k").doubleValue();
    t = getAncestorPar("t").doubleValue();
    T = getAncestorPar("T").doubleValue();
    p = getAncestorPar("p").doubleValue();

    int rows = getAncestorPar("rows").intValue();
    int cols = getAncestorPar("cols").intValue();
    int M = getAncestorPar("M").intValue();

    bsPositions = new Coord[nBS];
    transmitting = false;
    penalty = false;
    schedulePenalty = false;

    packetSent = registerSignal("packetSent");
    newPacket = registerSignal("newPacket");
    handover = registerSignal("handover");
    avoidHandover = registerSignal("avoidHandover");

    // Reference to own mobility module
    mobility = reinterpret_cast<TurtleMobility*> ( getModuleByPath("^.mobility") );

    for ( int i = 0; i < rows; i++ ) {
        for ( int j = 0; j < cols; j++ ) {
            bsPositions[i*rows+j].setX(M/2 + j*M);
            bsPositions[i*rows+j].setY(M/2 + i*M );
            EV<<"BS " << i*rows+j << " in position "<< bsPositions[i*rows+j]<<endl;
        }
    }
    scheduleAt( simTime(), new cMessage("Initialize"));
}

void Transmitter::handleMessage(cMessage *msg)
{
    if ( msg->isSelfMessage() ) {
        if ( strcmp(msg->getName(), "Initialize") == 0 ) {
            handleInitialize(msg);
        } else if ( strcmp(msg->getName(),"packetArrival") == 0 ) {
            handlePacketArrival(msg);
        } else if ( strcmp(msg->getName(),"checkHandover") == 0 ) {
            handleCheckHandover(msg);
        } else if ( strcmp(msg->getName(),"packetSent") == 0 ) {
            handlePacketSent(msg);
        } else if ( strcmp(msg->getName(),"penaltyTimeElapsed") == 0 ) {
            handlePenaltyTimeElapsed(msg);
        }
    }

}

void Transmitter::handleInitialize(cMessage *msg) {
    connectedBS = getClosestBS();
    EV<<"Closest BS: " << connectedBS <<endl;

    //Send first packet
    AircraftPacket* ap = new AircraftPacket("AircraftPacket");
    ap->setArrivalTime(simTime().dbl());
    ap->setAircraftID(getIndex());
    sendPacket(ap);

    // random offset in order to desynchronize aircrafts
    scheduleAt(simTime() + k + uniform(0,0.5), new cMessage("packetArrival")); // first packet generated
    scheduleAt(simTime() + t + uniform(0,5), new cMessage("checkHandover")); // Start handover period
    delete msg;
}

void Transmitter::handlePacketArrival(cMessage *msg) {
    EV<< "PacketArrival, queue length " << queue.length() << " transmitting " << transmitting <<endl;

    // Insert message into queue and schedule another arrival
    AircraftPacket* ap = new AircraftPacket("AircraftPacket");
    ap->setArrivalTime(simTime().dbl());
    ap->setAircraftID(getIndex());
    if ( !transmitting && !penalty ) {
        if ( queue.isEmpty() ) {
            EV<< "Queue is empty, sending packet"<<endl;
            sendPacket(ap);
        }
    } else {
        EV<< "Queuing"<<endl;
        queue.insert(ap);
        emit(newPacket, queue.length());
    }
    scheduleAt(simTime() + k, msg );
}

void Transmitter::handleCheckHandover(cMessage *msg) {
    int closest = getClosestBS();
    if ( connectedBS != closest ) {
        emit(handover,1);
        EV<<"HANDOVER, leaving "<< connectedBS<<", connecting to "<< closest <<endl;
        connectedBS = closest;
        penalty = true;
        if ( !transmitting ) {
            EV<< "Penalty started, waiting for: " << p<<"s"<<endl;
            scheduleAt(simTime() + p, new cMessage("penaltyTimeElapsed"));
        } else {
            EV<<"Penalty starting after finishing the current transmission "<<endl;
            schedulePenalty = true;
        }
    } else {
        EV<< "Handover avoided"<<endl;
        emit(avoidHandover,1);
    }
    scheduleAt(simTime() + t + uniform(0,5), msg); // Start handover period
}

void Transmitter::handlePacketSent(cMessage *msg) {
    EV<< "PacketSent with service time: "<< s <<endl;

    // s is the serviceTime computed for the last packet, who produced this PacketSent event
    emit(packetSent, s );

    transmitting = false;
    if ( !queue.isEmpty() && !penalty ) {
        AircraftPacket* ap = (AircraftPacket*) queue.front();
        queue.pop();
        sendPacket(ap);
    }

    if (schedulePenalty) {
        EV<< "Penalty started, waiting for: " << p<<"s"<<endl;
        scheduleAt(simTime() + p, new cMessage("penaltyTimeElapsed"));
        schedulePenalty = false;
    }
    delete msg;
}

void Transmitter::handlePenaltyTimeElapsed(cMessage *msg) {
    EV<<"Handover completed, transmissions restored" <<endl;
    penalty = false;

    // after penalty, check the queue to restart the transmission loop
    if ( !queue.isEmpty() && !penalty ) {
        AircraftPacket* ap = (AircraftPacket*) queue.front();
        queue.pop();
        sendPacket(ap);
    }

    delete msg;
}

void Transmitter::sendPacket(cPacket* pkt) {
    s = T*pow(bsPositions[connectedBS].distance(mobility->getCurrentPosition()),2);
    if ( s < 20 ) {
        send(pkt, "out", connectedBS);
        transmitting = true;
        scheduleAt(simTime() + s, new cMessage("packetSent"));
        EV<<"Sending packet  "<< pkt->getId() << " with service time "<< s <<endl;
    } else {
        // Probably wrap, then wrong distance, force handover and drop this packet ?
        int closest = getClosestBS();
        if ( connectedBS != closest ) {
            EV<<"FORCING HANDOVER, leaving "<< connectedBS<<", connecting to "<< closest <<endl;
            connectedBS = closest;
            penalty = true;
            EV<< "Penalty started, waiting for: " << p<<"s"<<endl;
            scheduleAt(simTime() + p, new cMessage("penaltyTimeElapsed"));
        }
        delete pkt;
    }
}

int Transmitter::getClosestBS() {
    Coord aircraftPosition = mobility->getCurrentPosition();
    double min = getAncestorPar("rows").intValue()*getAncestorPar("M").intValue();
    int closest;
    double distance;
    for ( int i = 0; i < nBS; i++ ) {
        distance = bsPositions[i].distance(aircraftPosition);
        EV<< "distance from " << i << " " << distance <<endl;
        if ( distance < min ) {
            min = distance;
            closest = i;
        }
    }
    EV<<"closest BS " << closest<<endl;
    return closest;
}

void Transmitter::finish() {
    queue.clear();
}

} //namespace
