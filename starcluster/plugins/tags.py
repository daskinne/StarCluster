import os
 
from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
 
class TagsPlugin(ClusterSetup):
    """
    Plugin that configures environment variables for a cluster
    """
    sg_prefix = 'SecurityGroup:@sc-'
    def __init__(self, tag_list=None,tag_file=None):
        tag_s = []
        if not tag_list is None:
            tag_s = [t.strip() for t in tag_list.split(',')]
        elif not tag_file is None:
            log.info("Adding tags from: %s " % tag_file)
            vfile_name = os.path.expanduser(tag_file or '') or None
            if vfile_name is not None: 
                fh = open(vfile_name,"r")
                line = fh.readline()
                while not line == "":
                    tag_s.append(line.strip().replace('\n',''))
                    line = fh.readline()
                fh.close()
        self.tags = dict([t.split('=') for t in tag_s])

    def run(self, nodes, master, user, user_shell, volumes):
        if not "cluster_assignment" in self.tags: 
            self.tags["cluster_assignment"] = master.parent_cluster.replace(self.sg_prefix,'');
        for tag in self.tags:
            val = self.tags.get(tag)
            log.info("Applying tag - %s: %s" % (tag, val))
            for node in nodes:
                node.add_tag(tag, val)

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        if not "cluster_assignment" in self.tags:
            self.tags["cluster_assignment"] = master.parent_cluster.replace(self.sg_prefix,'');
        for tag in self.tags:
            val = self.tags.get(tag)
            log.info("Applying tag - %s: %s" % (tag, val))
            for node in nodes:
                node.add_tag(tag, val)
