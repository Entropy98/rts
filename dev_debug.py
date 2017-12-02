def optimizationCheck(f):
    def g(*args):
        startTime=time.time()
        result=f(args)
        timeConsumed=time.time()-startTime
        if(f in data.functions):
            data.functions[f]['occur']+=1
            data.functions[f]['avgTime']=(data.functions[f]['avgTime']*(data.functions[f]['occur']-1)+timeConsumed)/data.functions[f]['occur']
        else:
            data.functions[f]=dict()
            data.functions[f]['occur']=1
            data.functions[f]=timeConsumed
        return result
    return g