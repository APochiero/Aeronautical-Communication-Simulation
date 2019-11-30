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
#include <string>

using namespace inet;
using namespace std;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize(int stage)
{
    nBS = par("nBS").intValue();
    mobility = reinterpret_cast<IMobility*> ( getModuleByPath(".mobility"));
//    EV<< mobility->getCurrentPosition().getX()<<endl;
    for ( int i = 0; i < nBS; i++ ) {
        string path = "bs[" + std::to_string(i) + "].mobility";
        bsMobilities.push_back(reinterpret_cast<IMobility*> (getModuleByPath(path.c_str())));
    }
//        EV << "Closest BS " << getClosestBS()<<endl;
}

void Transmitter::handleMessage(cMessage *msg)
{

}

int Transmitter::getClosestBS() {
    Coord aircraftPosition = mobility->getCurrentPosition();
    double max = 0;
    int closest;
    double distance;
    for ( int i = 0; i < nBS; i++ ) {
        Coord bsPosition = bsMobilities.at(i)->getCurrentPosition();
        distance = bsPosition.distance(aircraftPosition);
        if ( distance > max ) {
            max = distance;
            closest = i;
        }
    }
    return closest;
}

} //namespace
