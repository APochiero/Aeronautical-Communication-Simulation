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

#include "Waitress.h"

namespace barsimulator {

Define_Module(Waitress);

void Waitress::initialize()
{
    orderID = 0;
    orderDone = registerSignal("orderCompleted");

    if (par("sendInitialMessage").boolValue())
    {
        Order *msg = new Order(std::to_string(orderID++).c_str());
        msg->setIndex(uniform(0,3));
        scheduleAt(simTime(), msg);
    }
}

void Waitress::handleMessage(cMessage *msg)
{
    double period = 0.0;
    if ( msg->isSelfMessage() ) {
        EV << "Waitress sending new order " << msg->getName()<< endl;
        send(msg, "out");

        // Create a new Order
        Order *newOrder = new Order(std::to_string(orderID++).c_str());
        newOrder->setIndex( uniform(0,3) );
        newOrder->setTimestamp(simTime().dbl());
        newOrder->setStatus(0); // newOrder status

        period = uniform(0, 3);
        EV << "Waitress waiting new order for " << period << endl;
        scheduleAt(simTime() + period, newOrder);
    } else {
        Order* completedOrder = (Order*) msg;
        EV << "Waitress serving order with state: " << completedOrder->getStatus() << endl;
        emit(orderDone, simTime() - completedOrder->getTimestamp());
        delete msg;
    }
}

} //namespace
