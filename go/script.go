package main

import (
    "os"
    "log"
    "net/http"
    "time"
    "encoding/json"
    "strings"
)

var layout = "20060102T150405Z" //Date layout

func successResponse(w http.ResponseWriter, t1 time.Time, t2 time.Time, period string ) {
    utc, _ := time.LoadLocation("UTC") //UTC timezone
    var ptlist []string //slice containing the timestamps

    // truncate t1 based on period provided.
    if period == "1h" {
        t1 = t1.Add(1*time.Hour) //Add 1hour
        t1 = time.Date(t1.Year(), t1.Month(), t1.Day(), t1.Hour(), 0, 0, 0, t1.Location())
    } else if period == "1d" {
        t1 = t1.AddDate(0, 0, 1) //Add 1day
        t1 = time.Date(t1.Year(), t1.Month(), t1.Day(), 0, 0, 0, 0, t1.Location())
    } else if period == "1mo" { //https://pkg.go.dev/time#Time.AddDate AddDate normalizes its result in the same way that Date does, so, for example, adding one month to October 31 yields December 1, the normalized form for November 31.
        if t1.Month()==time.December {
            t1 = t1.AddDate(1, 0, 0) //Add 1 year and truncate others
            t1 = time.Date(t1.Year(), 1, 1, 0, 0, 0, 0, t1.Location())
        } else {
            t1 = time.Date(t1.Year(), t1.Month() + 1, 1, 0, 0, 0, 0, t1.Location())
        } 
    } else if period == "1y" {
        t1 = t1.AddDate(1, 0, 0) //Add 1year
        t1 = time.Date(t1.Year(), 1, 1, 0, 0, 0, 0, t1.Location())
    }
    date := t1 //will be used in the following loop so that ptlist will be filled.
    for date.Before(t2) { //while date < t2; date = date + period
        ptlist = append(ptlist, date.In(utc).Format(layout)) //append timestamps in UTC format and appropriate layout
        if period == "1h" {
            date = date.Add(1*time.Hour)
        } else if period == "1d" {
            date = date.AddDate(0, 0, 1)
        } else if period == "1mo" {
            if date.Month()==time.December {
                date = date.AddDate(1, 0, 0)
            } else {
                date = time.Date(date.Year(), date.Month() + 1, 1, 0, 0, 0, 0, t1.Location())
            }
        } else if period == "1y" {
            date = date.AddDate(1, 0, 0) //Add 1year
        }
    }
    jsonResp, err := json.MarshalIndent(ptlist, "", "  ")
    if err != nil {
        log.Fatalf("Error happened in JSON marshal. Err: %s", err)
    }
    w.Write(jsonResp)
    return
}

func errorResponse(w http.ResponseWriter, desc string) {
    w.WriteHeader(http.StatusBadRequest)
    resp := make(map[string]string)
    resp["desc"] = desc
    resp["status"] = "error"
    jsonResp, err := json.MarshalIndent(resp, "", "  ")
    if err != nil {
        log.Fatalf("Error happened in JSON marshal. Err: %s", err)
    }
    w.Write(jsonResp)
    return
}

func matchingTimestamps(w http.ResponseWriter, r *http.Request) {
    //p := fmt.Println
    if r.URL.Path != "/ptlist" {
            http.NotFound(w, r)
            return
    }
    switch r.Method {
    case "GET":
            w.Header().Set("Content-Type", "application/json")
            t1, ok1 := r.URL.Query()["t1"]
            t2, ok2 := r.URL.Query()["t2"]
            tz, ok3 := r.URL.Query()["tz"]
            period, ok4 := r.URL.Query()["period"]

            if !ok1 || !ok2 || !ok3 || !ok4 || len(r.URL.Query()) > 4 {
                errorResponse(w, "Malformed Query String")
                return
            }

            t1_utc, err := time.Parse(layout, strings.Join(t1,""))
            if err != nil {
                errorResponse(w, "Wrong Date Format Provided")
                return
            }
            t2_utc, err := time.Parse(layout, strings.Join(t2,""))
            if err != nil {
                errorResponse(w, "Wrong Date Format Provided")
                return
            }
            loc, err := time.LoadLocation(strings.Join(tz,""))
            if err != nil {
                errorResponse(w, "Unsupported TimeZone")
                return
            }
            period_check := (strings.Join(period,""))
            if period_check != "1h" && period_check !="1d" && period_check !="1mo" && period_check !="1y" {
                errorResponse(w, "Unsupported period")
                return
            }   
            t1_tz := t1_utc.In(loc) //Convert UTC in provided timezone
            t2_tz := t2_utc.In(loc) //Convert UTC in provided timezone
            successResponse(w, t1_tz, t2_tz, period_check)
            return
            //w.Write([]byte("Received a GET request\n"))
    default:
            w.WriteHeader(http.StatusNotImplemented)
            w.Write([]byte(http.StatusText(http.StatusNotImplemented)))
    }
}

func main() {
    http.HandleFunc("/", matchingTimestamps)
    log.Fatal(http.ListenAndServe(os.Args[1], nil))
}