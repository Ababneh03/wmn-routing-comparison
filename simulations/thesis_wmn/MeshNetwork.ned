package inet.examples.thesis_wmn;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.ManetRouter;
import inet.physicallayer.wireless.common.medium.RadioMedium;

network MeshNetwork {
    parameters:
        int numNodes;
        @display("bgb=1000,1000"); // Defines your 1000m x 1000m Area
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,100");
        }
        radioMedium: RadioMedium {
            @display("p=100,200");
        }
        host[numNodes]: ManetRouter {
            @display("p=500,500");
        }
}