#include <vector>
#include <map>
#include <cmath>
#include <cstdio>
#include <string>
#include <utility>
#include <algorithm>
using namespace std;

char in[1024];
typedef pair<int, double> partner;

bool comp(partner &a, partner &b)
{
    return a.second < b.second;
}

bool comp(partner &a, partner &b)
{
    return a.first < b.first;
}

void load_users(string fname, map<string, map<int, double> >&users)
{
    int cnt;
    int idx;
    double value;
    string key;
    FILE* ufile = fopen(fname.c_str(), "r");
    while(fscanf(ufile,"%s%d", in, &cnt)!=EOF)
    {
        key = string(in);
        //printf("%s %d\n", key.c_str(), cnt);
        users[key] = map<int, double>();
        for(int i=0;i<cnt;++i)
        {
            fscanf(ufile, "%d%lf", &idx, &value);
            users[key][idx] = value;
        }
    }    
    fclose(ufile);
}

void load_cluster(string fname, map<int, vector<string> >&clusters)
{
    int c_id;
    int cnt;
    FILE* cfile = fopen(fname.c_str(), "r");
    while(fscanf(cfile, "%d%d", &c_id, &cnt)!=EOF)
    {
        clusters[c_id] = vector<string>();
        for(int i=0;i<cnt;++i)
        {
            fscanf(cfile, "%s", in);
            clusters[c_id].push_back(string(in));
        }
    }
    fclose(cfile);
}

inline double cosine_distance(map<int, double> &a, map<int, double> &b)
{
    double dis = 0.0;
    double sz_a = 0.0, sz_b = 0.0;
    if(a.size() > b.size())
    {
        map<int, double>::iterator it;
        for(it=b.begin();it!=b.end();++it)
            if(a.find(it->first)!=a.end())
            {
                dis += (it->second)*a[it->first];
            }        
    }
    else
    {
        map<int, double>::iterator it;
        for(it=a.begin();it!=a.end();++it)
            if(b.find(it->first)!=b.end())
            {
                dis += (it->second)*b[it->first];
            }
    }

    map<int, double>::iterator it;
    for(it=a.begin();it!=a.end();++it)
        sz_a += (it->second)*(it->second);
    sz_a = sqrt(sz_a);
    for(it=b.begin();it!=b.end();++it)
        sz_b += (it->second)*(it->second);
    sz_b = sqrt(sz_b);
    dis /= sz_a;
    dis /= sz_b;
    return dis;
}

void generate_cluster_heap(map<int, vector<partner> > &cluster_dis,
                           map<int, vector<string> > &clusters,
                           map<string, map<int, double> > &users)
{
    cluster_dis.clear();
    map<int, vector<string> >::iterator it;
    map<int, vector<string> >::iterator jt;
    for(it = clusters.begin(); it!=clusters.end(); ++it)
    {
        cluster_dis[it->first] = vector<partner>();
    }
    
    for(it = clusters.begin(); it!=clusters.end(); ++it)
    {
        vector<string> &lst_1 = it->second;        
        for(jt = it, ++jt; jt!=clusters.end(); ++jt)
        {
            vector<string> &lst_2 = jt->second;
            double dis = 0.0;
            for(int i=0;i<lst_1.size();++i)
                for(int j=0;j<lst_2.size();++j)
                    dis += cosine_distance(users[lst_1[i]], users[lst_2[j]]);
            dis /= lst_1.size();
            dis /= lst_2.size();
            cluster_dis[it->first].push_back(partner(jt->first, dis));
            cluster_dis[jt->first].push_back(partner(it->first, dis));
        }        
    }
    map<int, vector<partner> >::iterator dt;
    for(dt=cluster_dis.begin();dt!=cluster_dis.end();++dt)
        std::make_heap(dt->second.begin(), dt->second.end(), comp);
}

void sub_clustering(map<int, vector<string> > &clusters,
                    map<int, vector<partner> > &cluster_dis)
{
    int max_id = 0;
    map<int, vector<string> >::iterator it;
    for(it=clusters.begin();it!=clusters.end();++it)
        if(max_id < (it->first))
            max_id = it->first;
    ++max_id;
    
    while(true)
    {
        double min = 1000000000.0;
        int min_a=0, min_b=0;
        map<int, vector<partner> >::iterator dt;
        for(dt=cluster_dis.begin();dt!=cluster_dis.end();++dt)
            if(min > (dt->second[0].second))
            {
                min_a = dt->first;
                min_b = dt->second[0].first;
            }
        //create new cluster
        //The clusters
        int new_id = max_id;
        ++max_id;
        clusters[new_id] = vector<string>();
        clusters[new_id].insert(clusters[new_id].end(), clusters[min_a].begin(),
                                clusters[min_a].end());
        clusters[new_id].insert(clusters[new_id].end(), clusters[min_b].begin(),
                                clusters[min_b].end());
        //The cluster_dis
        vector<partner> tmp;
        tmp.insert(tmp.end(), cluster_dis[min_a].begin(), cluster_dis[min_a].end());
        tmp.insert(tmp.end(), cluster_dis[min_b].begin(), cluster_dis[min_b].end());
        sort(tmp.begin(), tmp.end(), comp2);
        cluster_dis[new_id] = vector<partner>();
        for(dt=cluster_dis.begin();dt!=cluster_dis.end();++dt)
        {
            if(dt->first==min_a || dt->first==min_b) continue;
            dt->first = min_a;
            
        }
        //delete old cluster        
    }
}

int main()
{
    string fname = "users_info.dat";
    map<string, map<int, double> > users;
    load_users(fname, users);
    printf("%d\n", users.size());
    map<int, vector<string> > clusters;
    /*
    string fname2 = "clusters.dat";
    load_cluster(fname2, clusters);
    printf("%d\n", clusters.size());
    */

    map<string, map<int, double> > sub_users;
    map<string, map<int, double> >::iterator it;
    int cnt = 0;
    for(it = users.begin();it!=users.end() && cnt < 1000;++it, cnt++)
    {
        clusters[cnt] = vector<string>();
        clusters[cnt].push_back(it->first);
        sub_users[it->first] = it->second;
    }
    

    /*
    map<int, double> a;
    map<int, double> b;
    a[1] = 1.0;
    a[0] = 1.0;

    b[0] = 1.0;
    b[2] = 1.0;
    printf("cosine is %lf\n", cosine_distance(a, b));
    */
    map<int, vector<partner> > cluster_dis;
    generate_cluster_heap(cluster_dis, clusters, sub_users);
    printf("size of dis %d\n", cluster_dis.size());
    return 0;
}
