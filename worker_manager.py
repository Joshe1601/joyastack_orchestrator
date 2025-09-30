import random


class WorkerManager:
    def __init__(self, workers, ssh_user, ssh_pass):
        self.workers = workers  # dict con {worker1: {ip, ssh_port}, ...}
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass
        self.vm_inventory = []  # lista de dicts con info de VMs
        self.counter = 0

    def create_vms(self, num_vms):
        """
        Crea N VMs con distribución round-robin en los workers
        """
        worker_names = list(self.workers.keys())
        for i in range(num_vms):
            vm_id = i + 1
            wname = worker_names[i % len(worker_names)]
            wdata = self.workers[wname]

            print(f"\nConfiguración de VM{vm_id} (asignada a {wname})")
            cpus = int(input("   CPUs: "))
            ram = int(input("   RAM (MB): "))
            disk = int(input("   Disco (GB): "))
            vlan = int(input("   VLAN ID: "))

            vnc_port = vm_id  # VNC único
            mac_suffix = f"{random.randint(0, 255):02x}"  # Sufijo de MAC único para evitar conflictos

            vm_info = {
                "name": f"VM{vm_id}",
                "worker": wname,
                "ip": wdata["ip"],
                "ssh_port": wdata["ssh_port"],
                "cpus": cpus,
                "ram": ram,
                "disk": disk,
                "vlan": vlan,
                "vnc_port": vnc_port,
                "mac": f"20:19:37:33:ee:{mac_suffix}",  # OJO: acá la MAC empieza con mi código :V
            }

            # Aquí deberíamos ejecutar el script vm_create.sh en remoto pero por ahora simulamos
            print(
                f"{vm_info['name']} creada en {wname} "
                f"({wdata['ip']}:{wdata['ssh_port']})"
            )
            print(f"   CPUs={cpus}, RAM={ram}MB, DISK={disk}GB, VLAN={vlan}")
            print(
                f"   Acceso VNC (local): vnc://127.0.0.1:{30010 + vm_id}\n"
                f"   Ejecute en su PC:\n"
                f"   ssh -NL :{30010 + vm_id}:127.0.0.1:{5900 + vnc_port} "
                f"{self.ssh_user}@10.20.12.28 -p {wdata['ssh_port']}"
            )

            self.vm_inventory.append(vm_info)

    def list_vms(self):
        if not self.vm_inventory:
            print("No hay VMs desplegadas")
            return
        print("\n=== VMs desplegadas ===")
        for vm in self.vm_inventory:
            print(
                f"{vm['name']} en {vm['worker']} | "
                f"CPUs={vm['cpus']} RAM={vm['ram']}MB DISK={vm['disk']}GB "
                f"VLAN={vm['vlan']} VNC-Port={vm['vnc_port']}"
            )

    def reset_cluster(self):
        confirm = input("Seguro que deseas borrar todas las VMs? (yes/no): ")
        if confirm.lower() == "yes":
            print("Eliminando VMs...")
            self.vm_inventory = []  # Parar procesos QEMU
        else:
            print("Cancelado.")
