import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-2">Tailwind CSS + Shadcn/ui</h1>
          <p className="text-muted-foreground">Component library setup with dark theme</p>
          <div className="flex gap-2 justify-center mt-4">
            <Badge>Setup Complete</Badge>
            <Badge variant="secondary">Dark Mode</Badge>
            <Badge variant="outline">Ready</Badge>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Button Components</CardTitle>
            <CardDescription>Various button styles and variants</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-3">
            <Button>Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </CardContent>
        </Card>

        <Tabs defaultValue="forms" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="forms">Forms</TabsTrigger>
            <TabsTrigger value="accordion">Accordion</TabsTrigger>
            <TabsTrigger value="info">Info</TabsTrigger>
          </TabsList>
          <TabsContent value="forms">
            <Card>
              <CardHeader>
                <CardTitle>Form Components</CardTitle>
                <CardDescription>Input and textarea elements</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Input Field</label>
                  <Input placeholder="Type something..." />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Textarea Field</label>
                  <Textarea placeholder="Enter your message..." />
                </div>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Submit</Button>
              </CardFooter>
            </Card>
          </TabsContent>
          <TabsContent value="accordion">
            <Card>
              <CardHeader>
                <CardTitle>Accordion Component</CardTitle>
                <CardDescription>Collapsible content sections</CardDescription>
              </CardHeader>
              <CardContent>
                <Accordion type="single" collapsible className="w-full">
                  <AccordionItem value="item-1">
                    <AccordionTrigger>What is Tailwind CSS?</AccordionTrigger>
                    <AccordionContent>
                      Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-2">
                    <AccordionTrigger>What is Shadcn/ui?</AccordionTrigger>
                    <AccordionContent>
                      Shadcn/ui is a collection of re-usable components built using Radix UI and Tailwind CSS.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-3">
                    <AccordionTrigger>Why use these tools?</AccordionTrigger>
                    <AccordionContent>
                      They provide a great developer experience with accessible, customizable components and rapid development.
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="info">
            <Card>
              <CardHeader>
                <CardTitle>Configuration Info</CardTitle>
                <CardDescription>Setup details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Tailwind CSS</Badge>
                  <span className="text-sm text-muted-foreground">Installed and configured</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Shadcn/ui</Badge>
                  <span className="text-sm text-muted-foreground">Components ready</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Dark Mode</Badge>
                  <span className="text-sm text-muted-foreground">Default theme</span>
                </div>
                <div className="mt-4 p-4 bg-muted rounded-md">
                  <p className="text-sm font-mono">
                    Components: button, card, input, textarea, badge, tabs, accordion
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
