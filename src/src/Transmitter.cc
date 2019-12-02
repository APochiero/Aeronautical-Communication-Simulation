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
#include <algorithm>
#include "AircraftPacket_m.h"

using namespace inet;
using namespace std;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize(int stage) {
    switch(stage) {
        case 0: {
            nBS = par("nBS").intValue();
            k = getAncestorPar("k").doubleValue();
            t = getAncestorPar("t").doubleValue();
            T = getAncestorPar("T").doubleValue();
            p = getAncestorPar("p").doubleValue();

            int rows = getAncestorPar("rows").intValue();
            int cols = getAncestorPar("cols").intValue();
            int M = getAncestorPar("M").intValue();

            bsPositions = new Coord[nBS];   /* TODO shouldn't we share all these coordinates among all ACs? */
            transmitting = false;
            penalty = false;
            schedulePenalty = false;

            /* Registering all signals for stats */
            packetSent = registerSignal("packetSent");
            newPacket = registerSignal("newPacket");
            handover = registerSignal("handover");
            avoidHandover = registerSignal("avoidHandover");

            /* Reference to own mobility module */
            mobility = reinterpret_cast<TurtleMobility*> ( getModuleByPath("^.mobility") );

            /* setup base station positions */
            /* TODO -- shouldn't these coordinates be shared among all transmitters? */
            for ( int i = 0; i < rows; i++ ) {
                for ( int j = 0; j < cols; j++ ) {
                    bsPositions[i*rows+j].setX(M/2 + j*M);
                    bsPositions[i*rows+j].setY(M/2 + i*M );
                    EV<<"BS " << i*rows+j << " in position "<< bsPositions[i*rows+j]<<endl;
                }
            }
            break;
        }
        case 20: {   /* this stage nr comes surely after mobility module has been initialized */
            connectedBS = getClosestBS();

            // random offset in order to desynchronize aircrafts
            scheduleAt(simTime() + uniform(0, 5), new cMessage("desync"));
            break;
        }
    }
}

void Transmitter::handleMessage(cMessage *msg)
{
    if ( msg->isSelfMessage() ) {
        if ( strcmp(msg->getName(), "desync") == 0 ) {
            handleDesync(msg);
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

/* in order to avoid that all ACs transmitters are synced (that is not possible in a real scenario) */
void Transmitter::handleDesync(cMessage* msg) {
    EV << "==> Desync" << endl;

    // Send first packet
    AircraftPacket* ap = new AircraftPacket("AircraftPacket");
    ap->setArrivalTime(simTime().dbl());
    ap->setAircraftID(getIndex());
    sendPacket(ap);

    scheduleAt(simTime() + k, new cMessage("packetArrival")); // first packet generated
    scheduleAt(simTime() + t, new cMessage("checkHandover")); // start handover period
    delete msg;
}

void Transmitter::handlePacketArrival(cMessage *msg) {
    EV << "==> PacketArrival";
    EV << "queue length: " << queue.getLength() << ", transmitting: " << transmitting << endl;

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
        emit(newPacket, queue.getLength());
    }
    scheduleAt(simTime() + k, msg );
}

void Transmitter::handleCheckHandover(cMessage *msg) {
    EV << "==> CheckHandover" << endl;
    int closest = getClosestBS();
    if ( connectedBS != closest ) {
        emit(handover,1);
        EV << "HANDOVER, leaving " << connectedBS << ", connecting to "<< closest <<endl;
        connectedBS = closest;
        penalty = true;
        if ( !transmitting ) {
            EV << "Penalty started, waiting for: " << p << "s" <<endl;
            scheduleAt(simTime() + p, new cMessage("penaltyTimeElapsed"));
        } else {
            EV << "Penalty starting after finishing the current transmission" << endl;
            schedulePenalty = true;
        }
    } else {
        EV << "Handover avoided" << endl;
        emit(avoidHandover,1);
    }
    scheduleAt(simTime() + t, msg); // Start handover period
}

void Transmitter::handlePacketSent(cMessage *msg) {
    EV << "==> PacketSent with service time:" << s <<endl;

    // s is the serviceTime computed for the last packet, who produced this PacketSent event
    emit(packetSent, s);

    transmitting = false;
    if ( !queue.isEmpty() && !penalty ) {
        AircraftPacket* ap = (AircraftPacket*) queue.front();
        queue.pop();
        sendPacket(ap);
    }

    if (schedulePenalty) {
        EV << "Penalty started, waiting for: " << p << "s" <<endl;
        scheduleAt(simTime() + p, new cMessage("penaltyTimeElapsed"));
        schedulePenalty = false;
    }
    delete msg;
}

void Transmitter::handlePenaltyTimeElapsed(cMessage *msg) {
    EV << "==> PenaltyTimeElapsed: handover completed, transmissions restored" << endl;
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
    s = T*pow(getDistance(connectedBS), 2); /* formula given by specifications */
    send(pkt, "out", connectedBS);
    transmitting = true;
    scheduleAt(simTime() + s, new cMessage("packetSent"));
    EV << "==> SendPacket "<< pkt->getId() << " with service time "<< s <<endl;
}

int Transmitter::getClosestBS() {
    double min = getAncestorPar("rows").intValue() * getAncestorPar("M").intValue(); /* TODO don't we need to multiply this by sqrt(2) ? */
    int closest;
    double distance;
    for ( int i = 0; i < nBS; i++ ) {
        distance = getDistance(i);
        EV<< "distance from " << i << " " << distance <<endl;
        if ( distance < min ) {
            min = distance;
            closest = i;
        }
    }
    EV << "Closest BS " << closest <<endl;
    return closest;
}

/* computes distances between the Aircraft and the Base Station, taking in account a possible wrap around the region's edges */
double Transmitter::getDistance(int bs) {
    // get width/height of simulated region
    double L = getAncestorPar("rows").intValue() * getAncestorPar("M").intValue();

    const Coord acPos = mobility->getCurrentPosition();
    const Coord bsPosition = bsPositions[bs];

    /* simulate translation due to wrap around, and take smallest distance */
    vector<double> distances;
    distances.push_back(bsPosition.distance(acPos));
    distances.push_back(bsPosition.distance(acPos + Coord( L, 0)));
    distances.push_back(bsPosition.distance(acPos + Coord(-L, 0)));
    distances.push_back(bsPosition.distance(acPos + Coord(0,  L)));
    distances.push_back(bsPosition.distance(acPos + Coord(0, -L)));

    return *min_element(distances.begin(), distances.end());
}

void Transmitter::finish() {
    queue.clear();
}

// TODO do we need a destructor?

}
