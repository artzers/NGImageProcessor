
#include <pthread.h>
#include <QString>
#include <stdlib.h>
#include "NGThreadPool.h"

class MyThread:public IWorker
{
public:
    MyThread(std::string str):IWorker(),str_(str){}
    virtual ~MyThread(){}
    virtual void run(){
        //qsrand(0);
        srandom(0);
        int time = int(double(rand())/double(RAND_MAX)*5);
        sleep(time);
        printf("%s, sleep %d second\n", str_.c_str(), time);
    }
private:
    std::string str_;
};

void* Function_t(void* Param)
{
    printf("thread.\n");
    pthread_t myid = pthread_self();
    printf("thread ID=%d \n", myid);
    return NULL;
}

int main(int argc, char *argv[])
{
	
//    pthread_t pid1;
//    pthread_t pid2;
//    pthread_attr_t attr;
//    pthread_attr_init(&attr);
//    pthread_attr_setscope(&attr, PTHREAD_SCOPE_PROCESS);
//    //pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
//    pthread_create(&pid1, &attr, Function_t, NULL);
//    pthread_create(&pid2, &attr, Function_t, NULL);
//    pthread_join(pid1, NULL);
//    pthread_join(pid2, NULL);
//    printf("alldone.\n");
//    pthread_attr_destroy(&attr);
//    printf("alldone.\n");
    ThreadPool::Init(5);
    char line[256];
    printf("pool has %u threads\n", ThreadPool::GetThreadNum());
    for(int i = 0; i < 6; ++i){
        sprintf(line, "%d",i);
        std::string threadInfo = "this is job " + std::string(line);
        SmartIWorker job = SmartIWorker(new MyThread(threadInfo));
        ThreadPool::AddJob(job);
    }
    while(ThreadPool::GetJobNum() != 0){}
    ThreadPool::StopAll();
    printf("stop all\n");
    ThreadPool::Init(3);
    printf("pool has %u threads\n", ThreadPool::GetThreadNum());
    for(int i = 11; i < 14; ++i){
        sprintf(line, "%d",i);
        std::string threadInfo = "this is job " + std::string(line);
        SmartIWorker job = SmartIWorker(new MyThread(threadInfo));
        ThreadPool::AddJob(job);
    }
    sleep(2);
    ThreadPool::StopAll();
    printf("stop all\n");
    ThreadPool::Init(7);
    printf("pool has %u threads\n", ThreadPool::GetThreadNum());
    for(int i = 14; i < 22; ++i){
        sprintf(line, "%d",i);
        std::string threadInfo = "this is job " + std::string(line);
        SmartIWorker job = SmartIWorker(new MyThread(threadInfo));
        ThreadPool::AddJob(job);
    }
    sleep(2);
    ThreadPool::StopAll();
    printf("stop all\n");
    return 0;
}

