import { Fragment, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { connect, E, getAllLocalStorageItems, getRefValue, isTrue, preventDefault, processEvent, refs, uploadFiles } from "/utils/state"
import "focus-visible/dist/focus-visible"
import { Box, Button, Code, Heading, Link, Text, useColorMode, VStack } from "@chakra-ui/react"
import { MoonIcon, SunIcon } from "@chakra-ui/icons"
import NextLink from "next/link"
import NextHead from "next/head"


export default function Component() {
  const [state, setState] = useState({"is_hydrated": false, "events": [{"name": "state.hydrate"}], "files": []})
  const [result, setResult] = useState({"state": null, "events": [], "final": true, "processing": false})
  const [notConnected, setNotConnected] = useState(false)
  const router = useRouter()
  const socket = useRef(null)
  const { isReady } = router
  const { colorMode, toggleColorMode } = useColorMode()
  const focusRef = useRef();
  
  // Function to add new events to the event queue.
  const Event = (events, _e) => {
      preventDefault(_e);
      setState(state => ({
        ...state,
        events: [...state.events, ...events],
      }))
  }

  // Function to add new files to be uploaded.
  const File = files => setState(state => ({
    ...state,
    files,
  }))

  // Main event loop.
  useEffect(()=> {
    // Skip if the router is not ready.
    if (!isReady) {
      return;
    }

    // Initialize the websocket connection.
    if (!socket.current) {
      connect(socket, state, setState, result, setResult, router, ['websocket', 'polling'], setNotConnected)
    }

    // If we are not processing an event, process the next event.
    if (!result.processing) {
      processEvent(state, setState, result, setResult, router, socket.current)
    }

    // Reset the result.
    setResult(result => {
      // If there is a new result, update the state.
      if (result.state != null) {
        // Apply the new result to the state and the new events to the queue.
        setState(state => {
          return {
            ...result.state,
            events: [...state.events, ...result.events],
          } 
        })
        return {
          state: null,
          events: [],
          final: true,
          processing: !result.final,
        }
      }
      return result;
    })

    // Process the next event.
    processEvent(state, setState, result, setResult, router, socket.current)
  })

  // Set focus to the specified element.
  useEffect(() => {
    if (focusRef.current) {
      focusRef.current.focus();
    }
  })

  // Route after the initial page hydration.
  useEffect(() => {
    const change_complete = () => Event([E('state.hydrate', {})])
    router.events.on('routeChangeComplete', change_complete)
    return () => {
      router.events.off('routeChangeComplete', change_complete)
    }
  }, [router])


  return (
  <Fragment><Fragment>
  <Fragment>
  <Button onClick={toggleColorMode} sx={{"float": "right"}}>
  <Fragment>
  {isTrue((colorMode === "light")) ? (
  <Fragment>
  <SunIcon/>
</Fragment>
) : (
  <Fragment>
  <MoonIcon/>
</Fragment>
)}
</Fragment>
</Button>
  <VStack spacing="1.5em" sx={{"fontSize": "2em", "paddingTop": "10%"}}>
  <Heading sx={{"fontSize": "2em"}}>
  {`Welcome to Reflex!`}
</Heading>
  <Box>
  {`Get started by editing `}
  <Code sx={{"fontSize": "1em"}}>
  {`my_app_name/my_app_name.py`}
</Code>
</Box>
  <Link as={NextLink} href="https://reflex.dev/docs/getting-started/introduction" sx={{"border": "0.1em solid", "padding": "0.5em", "borderRadius": "0.5em", "_hover": {"color": isTrue((colorMode === "light")) ? `rgb(107,99,246)` : `rgb(179, 175, 255)`}}}>
  {`Check out our docs!`}
</Link>
</VStack>
</Fragment>
  <NextHead>
  <title>
  {`Reflex App`}
</title>
  <meta content="A Reflex app." name="description"/>
  <meta content="favicon.ico" property="og:image"/>
</NextHead>
</Fragment>
    </Fragment>
  )
}
