/*
* Copyright 2019-2020 VMware, Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://www.apache.org/licenses/LICENSE-2.0
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
 */
package api

import (
	"github.com/gin-gonic/gin"
)

const ServiceVersion = "v1.0.3"

type Version struct {
}

// Router is cluster router definition method
func (c *Version) Router(r *gin.RouterGroup) {

	authMiddleware, _ := GetAuthMiddleware()
	cluster := r.Group("/version")
	cluster.Use(authMiddleware.MiddlewareFunc())
	{
		cluster.GET("/", c.getVersion)
	}
}

func (_ *Version) getVersion(c *gin.Context) {
	c.JSON(200, gin.H{"msg": "getVersion success", "version": ServiceVersion})
}
