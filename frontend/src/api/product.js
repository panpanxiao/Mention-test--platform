import request from '@/utils/request'

export function apiProductList() {
  return request({
    url: '/api/product/list',
    method: 'get'
  })
}

// 调用项目增加接口
export function apiProductCreate(requestBody) {
  return request({
    url: '/api/product/create',
    method: 'post',
    data: requestBody
  })
}

export function apiProductUpdate(requestBody) {
  return request({
    url: '/api/product/update',
    method: 'post',
    data: requestBody
  })
}

// 调用真实删除数据库接口
export function apiProductDelete(id) {
  return request({
    url: '/api/product/delete',
    method: 'delete',
    params: {
      'id': id
    }
  })
}
// 条件查询
export function apiProductSearch(params) {
  return request({
    url: '/api/product/search',
    method: 'get',
    params: params
  })
}
