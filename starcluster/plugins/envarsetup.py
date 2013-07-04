import os
 
from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
 
class EnvarPlugin(ClusterSetup):
    """
    Plugin that configures environment variables for a cluster
    """
    var_str = ""
    def __init__(self, var_list=None,var_file=None):
        en_vars = []
        if not var_list is None:
            en_vars = var_list.strip().split(',')
        elif not var_file is None:
            log.info("Adding vars from: %s " % var_file)
            vfile_name = os.path.expanduser(var_file or '') or None
            if vfile_name is not None: 
                fh = open(vfile_name,"r")
                line = fh.readline()
                while not line == "":
                    en_vars.append(line.replace('\n',''))
                    line = fh.readline()
                fh.close()
        for var in en_vars:
            split_index = var.find('=')
            if not split_index == -1:
                self.var_str += 'export '+var[0:split_index].strip()+'="'+var[split_index+1:].strip().replace('"','\"')+'";\n'


    def run(self, nodes, master, user, user_shell, volumes):
        if not self.var_str == "":
            log.info("Setting environment variables on all nodes...")
            for node in nodes:
                nssh = node.ssh
                if not nssh.get_current_user() == 'root':
                    nssh.switch_user('root')
                env_file = nssh.remote_file('/etc/profile.d/scenv.sh','w+')
                env_file.write('\n'+self.var_str)
                env_file.close()

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        if not self.var_str == "":
            log.info("Setting environment variables on all nodes...")
            nssh = node.ssh
            if not nssh.get_current_user() == 'root':
                nssh.switch_user('root')
            env_file = nssh.remote_file('/etc/profile.d/scenv.sh','w+')
            env_file.write('\n'+self.var_str)
            env_file.close()