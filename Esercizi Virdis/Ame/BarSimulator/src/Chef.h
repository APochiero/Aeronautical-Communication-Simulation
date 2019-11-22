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

#ifndef __BARSIMULATOR_CHEF_H_
#define __BARSIMULATOR_CHEF_H_

#include <omnetpp.h>
#include <functional>
#include <queue>
#include <stack>
#include <vector>
#include "Order_m.h"


using namespace omnetpp;

namespace barsimulator {

/**
 * TODO - Generated class
 */
class Chef : public cSimpleModule
{
  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
    virtual void finish();
  private:
    simsignal_t arrival;
    double utilization;
    bool busyQueue;
//    bool busyStack;
//    bool busyGreater;
//    bool busyLess;

    std::queue<Order*> queue;
//    std::stack<Order*> stack;

//    struct greaterIndexFirst
//    {
//        bool operator()(const Order* o1, const Order* o2) const
//        {
//            return o1->getIndex() > o2->getIndex();
//        }
//    };
//    std::priority_queue<Order*, std::vector<Order*>, greaterIndexFirst> greaterPriority;

//    struct lessIndexFirst
//    {
//        bool operator()(const Order* o1, const Order* o2) const
//        {
//            return o1->getIndex() < o2->getIndex();
//        }
//    };
//    std::priority_queue<Order*, std::vector<Order*>, lessIndexFirst> lessPriority;
};

} //namespace

#endif
