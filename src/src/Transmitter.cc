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
#include "inet/mobility/contract/IMobility.h"

using namespace inet;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize(int stage)
{
    if ( stage == 11 ) { // a quanto pare ci sono 11 stage
        cModule *aircraft;
        aircraft = getParentModule();

        cModule *temp = (aircraft->getSubmodule("mobility"));
        mobility = reinterpret_cast<IMobility*> (temp);

        EV<< mobility->getCurrentPosition()<< endl;
    }
}

void Transmitter::handleMessage(cMessage *msg)
{

}

int Transmitter::getClosestBS() {

}

} //namespace
