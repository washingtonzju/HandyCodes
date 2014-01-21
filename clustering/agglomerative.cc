#include <vector>
#include <map>
#include <cmath>
#include <cstdio>
#include <string>
using namespace std;

char in[1024];
typedef pair<int, double> partner;

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
        users[key] = map<int, double>();
        for(int i=0;i<cnt;++i)
        {
            fscanf(ufile, "%d%lf", &idx, value);
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
        vector<string> &lst_1 = it->second;;
        for(jt = clusters.begin()+1; jt!=clusters.end(); ++jt)
        {
            vector<string> &lst_2 = jt->second;
            double dis = 0.0;
            for(int i=0;i<lst_1.size();++i)
                for(int j=0;j<lst_2.size();++j)
                    dis += cosine_distance(users[lst_1[i]], users[lst_2[j]]);
            dis /= lst_1.size();
            dis /= lst_2.size();
        }        
    }
}

void sub_clustering(map<string, vector<string> >&clusters,
                    map<int, vector<partner> &cluster_dis)
{
    
}

int main()
{
    string fname = "users_info.dat";
    map<string, map<int, double> > users;
    load_users(fname, users);
    printf("%d\n", users.size());
    map<string, vector<string> > clusters;
    /*
    string fname2 = "clusters.dat";
    load_cluster(fname2, clusters);
    printf("%d\n", clusters.size());
    */
    map<int, double> a;
    map<int, double> b;
    a[1] = 1.0;
    a[0] = 1.0;

    b[0] = 1.0;
    b[2] = 1.0;
    printf("cosine is %lf\n", cosine_distance(a, b));
    return 0;
}
