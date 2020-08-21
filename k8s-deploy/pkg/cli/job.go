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
package cli

import (
	"errors"
	"fmt"
	"github.com/FederatedAI/KubeFATE/k8s-deploy/pkg/db"
	"github.com/gosuri/uitable"
	"github.com/rs/zerolog/log"
	"helm.sh/helm/v3/pkg/cli/output"
	"os"
)

type Job struct {
}

func (c *Job) getRequestPath() (Path string) {
	return "job/"
}

func (c *Job) addArgs() (Args string) {
	return ""
}

type JobResultList struct {
	Data db.JobList
	Msg  string
}

type JobResult struct {
	Data *db.Job
	Msg  string
}

type JobResultMsg struct {
	Msg string
}

type JobResultErr struct {
	Error string
}

func (c *Job) getResult(Type int) (result interface{}, err error) {
	switch Type {
	case LIST:
		result = new(JobResultList)
	case INFO:
		result = new(JobResult)
	case MSG, JOB:
		result = new(JobResultMsg)
	case ERROR:
		result = new(JobResultErr)
	default:
		err = fmt.Errorf("no type %d", Type)
	}
	return
}

func (c *Job) outPut(result interface{}, Type int) error {
	switch Type {
	case LIST:
		return c.outPutList(result)
	case INFO:
		return c.outPutInfo(result)
	case MSG, JOB:
		return c.outPutMsg(result)
	case ERROR:
		return c.outPutErr(result)
	default:
		return fmt.Errorf("no type %d", Type)
	}
}

func (c *Job) outPutList(result interface{}) error {
	if result == nil {
		return errors.New("no out put data")
	}
	item, ok := result.(*JobResultList)
	if !ok {
		return errors.New("type jobResultList not ok")
	}

	joblist := item.Data
	joblist.Sort()

	table := uitable.New()
	table.AddRow("UUID", "CREATOR", "METHOD", "STATUS", "STARTTIME", "CLUSTERID")
	for _, r := range joblist {
		table.AddRow(r.Uuid, r.Creator, r.Method, r.Status.String(), r.StartTime.Format("2006-01-02 15:04:05"), r.ClusterId)
	}
	table.AddRow("")
	return output.EncodeTable(os.Stdout, table)
}

func (c *Job) outPutMsg(result interface{}) error {
	if result == nil {
		return errors.New("no out put data")
	}
	item, ok := result.(*JobResultMsg)
	if !ok {
		return errors.New("type JobResultMsg not ok")
	}

	_, err := fmt.Println(item.Msg)

	return err
}

func (c *Job) outPutErr(result interface{}) error {
	if result == nil {
		return errors.New("no out put data")
	}
	item, ok := result.(*JobResultErr)
	if !ok {
		return errors.New("type jobResultErr not ok")
	}

	_, err := fmt.Println(item.Error)

	return err
}

func (c *Job) outPutInfo(result interface{}) error {
	if result == nil {
		return errors.New("no out put data")
	}
	fmt.Printf("%+v", result)
	item, ok := result.(*JobResult)
	if !ok {
		return errors.New("type jobResult not ok")
	}
	fmt.Printf("%+v", item.Data)
	job := item.Data

	log.Debug().Interface("job", job).Msg("job info")

	table := uitable.New()

	table.AddRow("UUID", job.Uuid)
	table.AddRow("StartTime", job.StartTime.Format("2006-01-02 15:04:05"))
	table.AddRow("EndTime", job.EndTime.Format("2006-01-02 15:04:05"))
	table.AddRow("Status", job.Status.String())
	table.AddRow("Creator", job.Creator)
	table.AddRow("ClusterId", job.ClusterId)
	table.AddRow("Result", job.Result)
	table.AddRow("SubJobs", job.SubJobs)
	table.AddRow("")
	return output.EncodeTable(os.Stdout, table)
}
