from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ipv4

log = core.getLogger()

print("=== ✅ NEW QoS CONTROLLER LOADED ===")

def _handle_ConnectionUp(event):
    print("🔌 Switch connected, installing default rule")

    # Clear existing flows
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    event.connection.send(msg)

    # Send ALL packets to controller
    msg = of.ofp_flow_mod()
    msg.priority = 0
    msg.match = of.ofp_match()  # match everything
    msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    event.connection.send(msg)

def _handle_PacketIn(event):
    
    packet = event.parsed
    ip_packet = packet.find('ipv4')

    if ip_packet:
        print(f"📦 Packet Protocol: {ip_packet.protocol}")

        if ip_packet.protocol == 1:
            print("🔥 HIGH PRIORITY (ICMP)")

        elif ip_packet.protocol == 6:
            print("🐢 LOW PRIORITY (TCP)")

    # Just forward packet WITHOUT installing flow
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("QoS Controller Started")
