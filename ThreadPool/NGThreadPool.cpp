#include "NGThreadPool.h"

int ThreadPool::maxThreadNum_ = 0;
bool ThreadPool::shutdown_ = false;
pthread_mutex_t ThreadPool::lock_;// = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t ThreadPool::cond_;// = PTHREAD_COND_INITIALIZER;
std::vector<MyPThread> ThreadPool::threadList_;
std::vector<SmartIWorker> ThreadPool::jobList_;

ThreadPool::ThreadPool(void)//:maxThreadNum_(n)
{
}

ThreadPool::~ThreadPool(void)
{
}

bool ThreadPool::AddJob(SmartIWorker job)
{
    pthread_mutex_lock(&lock_);
    jobList_.push_back(job);
    //printf("add one job.\n");
    pthread_mutex_unlock(&lock_);
    pthread_cond_signal(&cond_);
    return true;
}

bool ThreadPool::AddJobList(const std::vector<SmartIWorker> jobList)
{
    pthread_mutex_lock(&lock_);
    std::copy(jobList.begin(), jobList.end(), std::back_inserter(jobList_));
    //printf("add one job.\n");
    pthread_mutex_unlock(&lock_);
    pthread_cond_signal(&cond_);
    return true;
}

bool ThreadPool::StopThreads(int num)
{
    if( int(GetThreadNum()) - num == 0){
        StopAll();
        return true;
    }else{
        for(size_t i = 0; i < num; ++i ){
            threadList_.back().open = false;
            pthread_cond_broadcast(&cond_);
            pthread_join(threadList_.back().id, NULL);
            threadList_.pop_back();
        }
    }
}

bool ThreadPool::StopAll()
{
    if (shutdown_) {printf("has shutdown.\n");return false;}
    printf("Now I will end all threads!!\n");
    /** wake up all thread */
    for (size_t i = 0; i < threadList_.size(); ++i)  {
        threadList_[i].open = false;
    }
    pthread_cond_broadcast(&cond_);
    for (size_t i = 0; i < threadList_.size(); ++i)  {
        pthread_join(threadList_[i].id, NULL);
    }
    threadList_.clear();

    pthread_mutex_destroy(&lock_);
    pthread_cond_destroy(&cond_);

    return true;
}

void ThreadPool::Init(int num)
{
    for (size_t i = 0; i < threadList_.size(); ++i)  {

    }
    if(threadList_.empty()){
        lock_ = PTHREAD_MUTEX_INITIALIZER;
        cond_ = PTHREAD_COND_INITIALIZER;
        threadList_.resize(num);
        for(size_t i = 0 ; i < threadList_.size(); ++i){
            threadList_[i].open = true;
            pthread_create(&(threadList_[i].id),NULL, ThreadFunc, &(threadList_.back()));
        }
    }else if(num < threadList_.size()){
        StopThreads(threadList_.size() - num);
    }else if(num > threadList_.size() && !threadList_.empty()){
        for(size_t i = 0; i < num - threadList_.size(); ++i){
            MyPThread tmp;
            tmp.open = true;
            threadList_.push_back(tmp);
            pthread_create(&(threadList_.back().id),NULL, ThreadFunc, &(threadList_.back()));
        }
    }
}

void *ThreadPool::ThreadFunc(void *param)
{
    bool &open = ((MyPThread*)param)->open;
    pthread_t tid = pthread_self();
    while (true){
        pthread_mutex_lock(&lock_);
        //ShutDownThread(pthread_self(), shutdown_, lock_);

        while (jobList_.empty() && open) {
            pthread_cond_wait(&cond_, &lock_);
        }

        ShutDownThread(pthread_self(), open, lock_);

        printf("tid %lu run\n", tid);

        /**
        *
        */
        SmartIWorker curWorker;
        if (!jobList_.empty()) {
            curWorker = jobList_.back();
            jobList_.pop_back();
        }

        pthread_mutex_unlock(&lock_);

        curWorker->run(); /** run job */
        printf("tid:%lu idle\n", tid);
    }
    return (void*)0;
}

