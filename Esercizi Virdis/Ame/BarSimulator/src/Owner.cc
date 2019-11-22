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

#include "Owner.h"
#include "Order_m.h"

namespace barsimulator {

Define_Module(Owner);

void Owner::initialize()
{
    first = true;
    interarrivalTime = registerSignal("arrival");
    cModule* kitchen = getParentModule();
    T = kitchen -> par("T");
}

void Owner::handleMessage(cMessage *msg)
{
    Order *newOrder = (Order*) msg;
    if ( newOrder->getStatus() == 0 ) {
        handleWaitressMessage(msg);
    } else if ( newOrder->getStatus() == 2 ) {
        // message coming from chefs
        handleChefMessage(msg);
    }
}

void Owner::handleWaitressMessage(cMessage *msg) {
    EV<< "Owner receiving new order"<<endl;
    Order *newOrder = (Order*) msg;

    double v = newOrder->getIndex();

    if ( first ) {
        previousTime = simTime().dbl();
        first = false;
    } else {
        // Compute interarrivalTime
       double currentTime = simTime().dbl();
       double interarrival = currentTime - previousTime;
       EV<< "Owner INTERARRIVAL:  "<< interarrival <<endl;
       emit(interarrivalTime, interarrival );
       previousTime = currentTime;
    }
    newOrder->setStatus(1); // Owner received the order
    if ( v >= T) {
        EV<< "Owner sending order to chef 1 ( index: "<< v << " )"<< endl;
        send(newOrder, "out", 0);
    } else {
        EV<< "Owner sending order to chef 2 ( index: "<< v << " )"<< endl;
        send(newOrder, "out", 1);
    }
}

void Owner::handleChefMessage(cMessage *msg) {
    EV<< "Owner calling waitress"<< endl;
    Order* order = (Order*) msg;
    order->setStatus(3); // Owner received the completed order
    send(order, "out", 2);
}
}//namespace
