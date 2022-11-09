
const install = (Vue, vm) => {

	// hello world
	vm.$api.dakacount 			= async (params = {}) => await vm.$u.http.get('/api/count', {params : params});
	
	vm.$api.submit 				= async (params = {}) => await vm.$u.http.get('/api/submit',  {params : params});
	vm.$api.query 				= async (params = {}) => await vm.$u.http.get('/api/query',  {params : params});
	vm.$api.stop 				= async (params = {}) => await vm.$u.http.get('/api/stop',  {params : params});
	
}

export default {
	install
}
