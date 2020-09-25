import axios from 'axios';

const host = 'http://127.0.0.1:8000';
export default host;
axios.defaults.baseURL = host;

// 登录
export const login = params => { return axios.post(`user/login/`, params) };

// 注册
export const register = params => { return axios.post(`user/register/`, params) };

// 判断用户名是否注册
export const check_username = username => { return axios.get(`user/` + username + '/count/') };

// 判断邮箱是否注册
export const check_email = email => { return axios.get(`user/` + email + '/count/') };

// 获取项目列表信息
export const projects_list = params => { return axios.get(`projects/?page=` + params.page + '&size=' + params.size) };

// 删除某个项目
export const delete_project = id => { return axios.delete(`projects/` + id + '/') };

// 修改某个项目
export const edit_project = (id, params) => { return axios.put(`projects/` + id + '/', params) };

// 新增项目
export const add_project = params => { return axios.post(`projects/`, params) };

// 获取所有项目ID和名称
export const projects_names = () => { return axios.get(`projects/names/`) };

// 获取所有环境变量的ID和名称
export const envs_names = () => { return axios.get(`envs/names/`) };

// 通过项目来运行用例
export const run_by_project = (project_id, datas) => { return axios.post(`projects/` + project_id + '/run/', datas) };

// 新增内置函数
export const add_builtin = params => { return axios.post(`debugtalks/`, params) };

// 获取内置函数列表信息
export const builtins_list = params => { return axios.get(`debugtalks/?page=` + params.page + '&size=' + params.size) };

// 获取内置函数名称
export const builtins_names = params => { return axios.get(`debugtalks/names/`) };

// 获取内置函数源码
export const builtins_code = id => { return axios.get(`debugtalks/` + id + '/') };

// 修改指定的内置函数源码
export const builtins_update = (id, code) => { return axios.put(`debugtalks/` + id + '/', { 'debugtalk': code }) };

//删除指定内置函数
export const builtin_delete = id => { return axios.delete(`debugtalks/` + id + '/') };

// 获取模块列表信息
export const modules_list = params => { return axios.get(`modules/?page=` + params.page + '&size=' + params.size) };

// 删除某个模块
export const delete_module = id => { return axios.delete(`modules/` + id + '/') };

// 修改某个模块
export const edit_module = (id, params) => { return axios.put(`modules/` + id + '/', params) };

// 新增模块
export const add_module = params => { return axios.post(`modules/`, params) };

// 通过模块来运行用例
export const run_by_module = (module_id, datas) => { return axios.post(`modules/` + module_id + '/run/', datas) };

// 获取套件列表信息
export const testsuites_list = params => { return axios.get(`testsuites/?page=` + params.page + '&size=' + params.size) };

// 删除某个套件
export const delete_testsuite = id => { return axios.delete(`testsuites/` + id + '/') };

// 新增套件
export const add_testsuite = params => { return axios.post(`testsuites/`, params) };

// 获取套件详情
export const get_detail_testsuite = id => { return axios.get(`testsuites/` + id + '/') };

// 修改套件
export const update_testsuite = (id, params) => { return axios.put(`testsuites/` + id + '/', params) };


// 通过套件来运行用例
export const run_by_testsuite = (testsuite_id, datas) => { return axios.post(`testsuites/` + testsuite_id + '/run/', datas) };

// 获取某个项目下的所有模块信息
export const modules_by_project_id = id => { return axios.get(`projects/` + id + '/modules/') };

// 获取用例列表信息
export const testcases_list = params => { return axios.get(`testcases/?page=` + params.page + '&size=' + params.size) };

// 删除某个用例
export const delete_testcase = id => { return axios.delete(`testcases/` + id + '/') };


// 获取某个模块下的所有用例信息
export const testcases_by_module_id = id => { return axios.get(`modules/` + id + '/testcases/') };

// 新增用例
export const add_testcase = params => { return axios.post(`testcases/`, params) };

// 运行用例
export const run_by_testcase = (testcase_id, env_id) => { return axios.post(`testcases/` + testcase_id + '/run/', { 'env_id': env_id }) };

//调试用例
export const debug = params => { return axios.post(`testcases/debug/`, params) };
//复制用例
export const copy_testcase = (id, copy_name) => { return axios.post(`testcases/` + id + '/copy_testcase/', { 'name': copy_name }) };
// 获取用例详情

export const get_detail_testcase = id => { return axios.get(`testcases/` + id + '/') };

// 修改用例
export const update_testcase = (id, params) => { return axios.put(`testcases/` + id + '/', params) };

//上传文件
export const upload_file = params => { return axios.post(`testcases/upload_file/`,params) };

// 获取测试报告列表信息
export const reports_list = params => { return axios.get(`reports/?ordering=-id&page=` + params.page + '&size=' + params.size) };

// 删除某个测试报告
export const report_delete = id => { return axios.delete(`reports/` + id + '/') };

// 下载测试报告
export const report_download = id => {
    return axios.get(`reports/` + id + '/download/',
        {
            responseType: 'blob'
        });
};

// 打开测试报告
// export const report_open = id => { return axios.get(`/reports/` + id + '/open/') };
export const report_view = id => { return axios.get(`reports/` + id + '/') };

// 获取配置列表信息
export const configures_list = params => { return axios.get(`configures/?page=` + params.page + '&size=' + params.size) };
//获取全部配置
export const configures_all = params => { return axios.get(`configures/names`) };

// 删除某个配置
export const delete_configure = id => { return axios.delete(`configures/` + id + '/') };

// 新增配置
export const add_configure = params => { return axios.post(`configures/`, params) };

// 获取配置详情
// export const get_detail_configure = id => { return axios.get(`/configures/`+ id + '/details/') };
export const get_detail_configure = id => { return axios.get(`configures/` + id + '/') };

// 修改配置
export const update_configure = (id, params) => { return axios.put(`configures/` + id + '/', params) };

// 获取环境列表信息
export const envs_list = params => { return axios.get(`envs/?page=` + params.page + '&size=' + params.size) };

// 删除某个环境
export const delete_env = id => { return axios.delete(`envs/` + id + '/') };

// 修改某个环境
export const edit_env = (id, params) => { return axios.put(`envs/` + id + '/', params) };

// 新增环境
export const add_env = params => { return axios.post(`envs/`, params) };

// 获取所有统计信息
export const summary = () => { return axios.get(`summary/`) };

// 获取所有压力测试列表信息
export const locusts_list = params => { return axios.get(`locusts/?page=` + params.page + '&size=' + params.size) };

// 新增压力测试
export const add_locust = params => { return axios.post(`locusts/`, params) };

// 获取压力测试详情
export const get_detail_locust = id => { return axios.get(`locusts/` + id + '/') };

// 修改压力测试
export const update_locust = (id, params) => { return axios.put(`locusts/` + id + '/', params) };

// 删除压力测试
export const locust_delete = id => { return axios.delete(`locusts/` + id + '/') };

//解除端口占用
export const kill_port = () => { return axios.post(`locusts/kill/`) };

//运行压力测试
export const run_locust = (locust_id, datas) => { return axios.post(`locusts/` + locust_id + '/run/', datas) };

export const run_locust_noweb = (locust_id, datas) => { return axios.post(`locusts/` + locust_id + '/run_noweb/', datas) };
//获取Mock列表
export const interfacemock_list = params => { return axios.get(`interfacemocks/?page=` + params.page + '&size=' + params.size) };

export const get_detail_interfacemock = id => { return axios.get(`interfacemocks/` + id + '/') };

export const add_interfacemock = params => { return axios.post(`interfacemocks/`, params) };

export const patch_interfacemock = (id, params) => { return axios.patch(`interfacemocks/` + id + '/', params) };

export const update_interfacemock = (id, params) => { return axios.put(`interfacemocks/` + id + '/', params) };

export const delele_interfacemock = id => { return axios.delete(`interfacemocks/` + id + '/') };

// 获取某个Mock接口的详情
export const mocks_list = id => { return axios.get(`interfacemocks/` + id + '/mocks/') };


//Mock场景信息
export const get_detail_mock = id => { return axios.get(`mocks/` + id + '/') };

export const add_mock = params => { return axios.post(`mocks/`, params) };

export const patch_mock = (id, params) => { return axios.patch(`mocks/` + id + '/', params) };

export const update_mock = (id, params) => { return axios.put(`mocks/` + id + '/', params) };

export const delele_mock = id => { return axios.delete(`mocks/` + id + '/') };

export const restart_mock = () => { return axios.post(`interfacemocks/restart/`) };


