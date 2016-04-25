#ifndef NGTHREADPOOL
#define NGTHREADPOOL
#include <pthread.h>
#include <vector>
#include <memory>

class IWorker;
typedef std::shared_ptr<IWorker> SmartIWorker;
class IWorker
{
public:
    IWorker(){}
    virtual ~IWorker(){}
	virtual void run()=0;

protected:

private:
	//unsigned long  m_ThreadID;
	//pthread_t  pThread_;
};

struct MyPThread{
    bool open;
    pthread_t id;
};

class ThreadPool;
typedef std::shared_ptr<ThreadPool> SmartThreadPool;

class ThreadPool
{
public:
    //static SmartThreadPool New(int p=0){return SmartThreadPool(new ThreadPool(p));}
    ~ThreadPool(void);

    static void Init(int);
    static bool AddJob(SmartIWorker job);
    static bool StopAll();
    static size_t GetJobNum(){return jobList_.size();}
   static size_t GetThreadNum(){return threadList_.size();}
   static bool StopThreads(int num);
   static bool AddJobList(const std::vector<SmartIWorker> jobList);
protected:
    ThreadPool(void );
    static void* ThreadFunc(void * threadData);

private:
    static bool shutdown_;
    static int maxThreadNum_;

    static pthread_mutex_t lock_;
    static pthread_cond_t cond_;

    static std::vector<MyPThread> threadList_;
    static std::vector<SmartIWorker> jobList_;
};

#define ShutDownThread( id,  open,  mutex) \
    if (!open) { \
        pthread_mutex_unlock(&mutex); \
        printf("thread %lu will exit\n", id); \
        pthread_exit(NULL); \
    }

#endif
