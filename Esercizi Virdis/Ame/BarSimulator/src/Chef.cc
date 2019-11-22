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

#include "Chef.h"
#include "Order_m.h"

namespace barsimulator {

Define_Module(Chef);

void Chef::initialize()
{
    arrival = registerSignal("arrival");
    utilization = 0.0;
    busyQueue = false;
//    busyStack = false;
//    busyGreater = false;
//    busyLess = false;
}

void Chef::handleMessage(cMessage *msg)
{
    Order* newOrder = (Order*) msg;

    if ( newOrder->getStatus() != 1 ) {
        EV << "BAD ORDER STATUS" <<endl;
        return;
    }

    if ( msg->isSelfMessage() ) {
        // sending order completed
        EV<< this->getName() << " order completed "<< endl;
        newOrder->setStatus(2); // order completed
        send(newOrder, "out");
        busyQueue = false;
//        busyStack = false;
//        busyGreater = false;
//        busyLess = false;
    } else {
        emit(arrival, 1);
        utilization += newOrder->getIndex();
        EV<< this->getName() << " queueing order "<< newOrder->getName()<< endl;
        queue.push(newOrder);
//        stack.push(newOrder);
//        greaterPriority.push(newOrder);
//        lessPriority.push(newOrder);
    }

    // take another order
    if ( !busyQueue && !queue.empty() ) {
        busyQueue = true;
        Order* nextOrder = queue.front();
        EV<< this->getName() << " cooking "<< nextOrder->getName()<< endl;
        scheduleAt( simTime() + nextOrder->getIndex(), nextOrder);
        queue.pop();
    }

//    if ( !busyStack && !stack.empty() ) {
//        busyStack = true;
//        Order* nextOrder = stack.top();
//        EV<< this->getName() << " cooking "<< nextOrder->getName()<< endl;
//        scheduleAt( simTime() + nextOrder->getIndex(), nextOrder);
//        stack.pop();
//    }

//    if ( !busyGreater && !greaterPriority.empty() ) {
//        busyGreater = true;
//        Order* nextOrder = greaterPriority.top();
//        EV<< this->getName() << " cooking "<< nextOrder->getName()<< endl;
//        scheduleAt( simTime() + nextOrder->getIndex(), nextOrder);
//        greaterPriority.pop();
//    }

//    if ( !busyLess && !lessPriority.empty() ) {
//        busyLess = true;
//        Order* nextOrder = lessPriority.top();
//        EV<< this->getName() << " cooking "<< nextOrder->getName()<< " " << nextOrder->getIndex() << endl;
//        scheduleAt( simTime() + nextOrder->getIndex(), nextOrder);
//        lessPriority.pop();
//    }
}

void Chef::finish() {
    EV<< this->getName()<<" utilization: " << utilization/simTime() << endl;
}

} //namespace
