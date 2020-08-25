package api

import (
	"encoding/json"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func Get(uri string, router *gin.Engine) *httptest.ResponseRecorder {
	// construct get
	req := httptest.NewRequest("GET", uri, nil)
	// init
	w := httptest.NewRecorder()
	// get handler
	router.ServeHTTP(w, req)
	return w
}
func TestAPI(t *testing.T) {
	body := gin.H{
		"msg": "kubefate run success",
	}
	router := initGinEngine()
	var w *httptest.ResponseRecorder
	url := "/"
	w = Get(url, router)
	assert.Equal(t, 200, w.Code)

	// convert the JSON response to a map
	var response map[string]string
	// grab the value & whether or not it exists
	err := json.Unmarshal([]byte(w.Body.String()), &response)
	value, exists := response["msg"]

	// Make some assertions on the correctness of the response.
	assert.Nil(t, err)
	assert.True(t, exists)
	assert.Equal(t, body["msg"], value)

	urlv1 := "/v1/"
	w = Get(urlv1, router)
	assert.Equal(t, 400, w.Code)
}

// func TestJob(t *testing.T) {
// 	router := initGinEngine()
// 	var w *httptest.ResponseRecorder
// 	url := "/job/"
// 	w = Get(url, router)
// 	assert.Equal(t, 200, w.Code)
// }
