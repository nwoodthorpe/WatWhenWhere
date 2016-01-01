import sys, ast, getopt, types
import collision

def main(argv):            
    arg_dict={}
    switches={'li':list,'di':dict,'tu':tuple}
    singles=''.join([x[0]+':' for x in switches])
    long_form=[x+'=' for x in switches]
    d={x[0]+':':'--'+x for x in switches}
    try:            
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError:          
        print "bad arg"                       
        sys.exit(2)       
    for opt, arg in opts:        
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o =''
        if o and arg:
            arg_dict[o]=ast.literal_eval(arg)

        if not o or not isinstance(arg_dict[o], switches[o]):    
            print opt, arg, " Error: bad arg"
            sys.exit(2)                 

    for e in arg_dict:
        print collision.collide(arg_dict[e])
        return collision.collide(arg_dict[e])     

if __name__ == '__main__':
    main(sys.argv[1:]) 
